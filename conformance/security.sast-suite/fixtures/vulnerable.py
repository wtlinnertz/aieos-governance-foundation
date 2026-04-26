"""Fixture: deliberately-introduced SAST findings.

This file contains patterns conformant SAST adapters should flag at least
one of. The exact rule depends on the underlying tool's ruleset; the
suite's criterion is schema_conformance (output validates against the
SARIF schema), not a specific rule match.
"""

import os
import subprocess


def run_user_command(cmd: str) -> str:
    # Classic SAST trigger: shell=True with a user-controlled argument.
    return subprocess.check_output(cmd, shell=True).decode()


def read_secret() -> str:
    # Hard-coded credential pattern — most SAST + secret-scan tools flag this.
    api_key = "sk-deliberate-fixture-key-do-not-trust"
    return api_key


def password_hash(password: str) -> str:
    # Deprecated weak hash — common SAST flag.
    import hashlib

    return hashlib.md5(password.encode()).hexdigest()
