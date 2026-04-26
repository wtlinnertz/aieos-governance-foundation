"""Fixture: deliberately-included secret-shaped strings.

Patterns that secret-scanners flag. The fixture is for shape conformance —
adapter output validates against SARIF; whether a specific scanner flags
each pattern depends on its ruleset.
"""

# Conventional API key shape
OPENAI_API_KEY = "sk-fixture0000000000000000000000000000000000000000"

# AWS access key id pattern (length + AKIA prefix)
AWS_ACCESS_KEY_ID = "AKIAFIXTUREKEYAAAAAA"
AWS_SECRET_ACCESS_KEY = "fixtureSecretFixtureSecretFixtureSecret00"

# Generic high-entropy token
GITHUB_TOKEN = "ghp_FixtureTokenFixtureTokenFixtureToken12345"

# Private key marker (most secret scanners flag this header)
PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
fixtureKeyMaterialDoNotTrust
-----END PRIVATE KEY-----
"""
