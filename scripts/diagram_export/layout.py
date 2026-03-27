"""Grid-based positioning algorithm for Diagram models.

No external dependencies. Uses BFS-based topological layering to assign
nodes to layers, then positions them on a grid with spacing constants.
Subgraphs are sized to contain their children with padding.
"""
from __future__ import annotations

from collections import defaultdict, deque

from .models import Diagram, Node, Subgraph

# Grid spacing constants
H_SPACING = 160  # Horizontal gap between layers
V_SPACING = 100  # Vertical gap between nodes in same layer
SUBGRAPH_PADDING = 40  # Padding inside subgraph containers
SUBGRAPH_HEADER = 30  # Height of subgraph title bar
MIN_NODE_WIDTH = 120
CHARS_PER_EXTRA_PX = 8  # Add width for long labels


def _compute_node_size(node: Node) -> None:
    """Size a node based on its label length and shape."""
    # Strip HTML tags for length calculation
    clean_label = node.label.replace("<br/>", " ").replace("<br>", " ")

    if node.shape == "diamond":
        size = max(80, len(clean_label) * 6 + 20)
        node.width = size
        node.height = size
    elif node.shape == "circle":
        size = max(60, len(clean_label) * 6 + 20)
        node.width = size
        node.height = size
    else:
        node.width = max(MIN_NODE_WIDTH, len(clean_label) * CHARS_PER_EXTRA_PX + 40)
        node.height = 60


def layout_diagram(diagram: Diagram) -> None:
    """Position all nodes and subgraphs in the diagram. Modifies in place."""
    if not diagram.nodes:
        return

    # ------------------------------------------------------------------
    # Step 1: Build adjacency lists
    # ------------------------------------------------------------------
    successors: dict[str, list[str]] = defaultdict(list)
    predecessors: dict[str, list[str]] = defaultdict(list)

    for edge in diagram.edges:
        if edge.source in diagram.nodes and edge.target in diagram.nodes:
            successors[edge.source].append(edge.target)
            predecessors[edge.target].append(edge.source)

    # ------------------------------------------------------------------
    # Step 2: BFS from roots to assign layers
    # ------------------------------------------------------------------
    all_node_ids = set(diagram.nodes.keys())
    roots = [nid for nid in all_node_ids if nid not in predecessors]

    # If no roots (cycle), pick all nodes as roots
    if not roots:
        roots = list(all_node_ids)

    layer_of: dict[str, int] = {}
    queue: deque[str] = deque()

    for r in roots:
        if r not in layer_of:
            layer_of[r] = 0
            queue.append(r)

    while queue:
        nid = queue.popleft()
        current_layer = layer_of[nid]
        for succ in successors.get(nid, []):
            # Assign successor to at least one layer deeper
            new_layer = current_layer + 1
            if succ not in layer_of or layer_of[succ] < new_layer:
                layer_of[succ] = new_layer
                queue.append(succ)

    # Any disconnected nodes not yet assigned get layer 0
    for nid in all_node_ids:
        if nid not in layer_of:
            layer_of[nid] = 0

    # ------------------------------------------------------------------
    # Step 3: Size nodes
    # ------------------------------------------------------------------
    for node in diagram.nodes.values():
        _compute_node_size(node)

    # ------------------------------------------------------------------
    # Step 4: Group nodes by layer and position
    # ------------------------------------------------------------------
    layers: dict[int, list[str]] = defaultdict(list)
    for nid, layer in layer_of.items():
        layers[layer].append(nid)

    # Sort nodes within each layer for deterministic output
    for layer_nodes in layers.values():
        layer_nodes.sort()

    is_horizontal = diagram.direction in ("LR", "RL")

    for layer_idx in sorted(layers.keys()):
        layer_nodes = layers[layer_idx]
        for pos_idx, nid in enumerate(layer_nodes):
            node = diagram.nodes[nid]
            if is_horizontal:
                node.x = layer_idx * H_SPACING
                node.y = pos_idx * V_SPACING
            else:
                node.x = pos_idx * H_SPACING
                node.y = layer_idx * V_SPACING

    # ------------------------------------------------------------------
    # Step 5: Size and position subgraphs around children
    # ------------------------------------------------------------------
    # Process subgraphs bottom-up (leaves first) so nested subgraphs
    # are sized before their parents.
    processing_order = _subgraph_bottom_up_order(diagram)

    for sg_id in processing_order:
        sg = diagram.subgraphs[sg_id]
        _size_subgraph(diagram, sg)


def _subgraph_bottom_up_order(diagram: Diagram) -> list[str]:
    """Return subgraph IDs in bottom-up order (leaf subgraphs first)."""
    # Build parent→children mapping for subgraphs
    sg_children: dict[str, list[str]] = defaultdict(list)
    sg_roots: list[str] = []

    for sg_id, sg in diagram.subgraphs.items():
        if sg.parent and sg.parent in diagram.subgraphs:
            sg_children[sg.parent].append(sg_id)
        else:
            sg_roots.append(sg_id)

    # BFS to get top-down order, then reverse
    order: list[str] = []
    queue: deque[str] = deque(sg_roots)
    while queue:
        sg_id = queue.popleft()
        order.append(sg_id)
        for child_id in sg_children.get(sg_id, []):
            queue.append(child_id)

    order.reverse()
    return order


def _size_subgraph(diagram: Diagram, sg: Subgraph) -> None:
    """Compute subgraph position and size from its children."""
    if not sg.children:
        # Empty subgraph — give it a minimal size
        sg.width = MIN_NODE_WIDTH + 2 * SUBGRAPH_PADDING
        sg.height = 60 + 2 * SUBGRAPH_PADDING + SUBGRAPH_HEADER
        return

    # Collect bounding boxes of all children (nodes and nested subgraphs)
    min_x = float("inf")
    min_y = float("inf")
    max_right = float("-inf")
    max_bottom = float("-inf")

    for child_id in sg.children:
        if child_id in diagram.nodes:
            node = diagram.nodes[child_id]
            min_x = min(min_x, node.x)
            min_y = min(min_y, node.y)
            max_right = max(max_right, node.x + node.width)
            max_bottom = max(max_bottom, node.y + node.height)
        elif child_id in diagram.subgraphs:
            child_sg = diagram.subgraphs[child_id]
            min_x = min(min_x, child_sg.x)
            min_y = min(min_y, child_sg.y)
            max_right = max(max_right, child_sg.x + child_sg.width)
            max_bottom = max(max_bottom, child_sg.y + child_sg.height)

    if min_x == float("inf"):
        # No valid children found
        sg.width = MIN_NODE_WIDTH + 2 * SUBGRAPH_PADDING
        sg.height = 60 + 2 * SUBGRAPH_PADDING + SUBGRAPH_HEADER
        return

    # Position subgraph around children with padding
    sg.x = min_x - SUBGRAPH_PADDING
    sg.y = min_y - SUBGRAPH_PADDING - SUBGRAPH_HEADER
    sg.width = (max_right - min_x) + 2 * SUBGRAPH_PADDING
    sg.height = (max_bottom - min_y) + 2 * SUBGRAPH_PADDING + SUBGRAPH_HEADER
