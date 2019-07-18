import subprocess
import sys

import mario.aliasing
import pytest

import mario_addons.plugins.addons


ALIASES = mario_addons.plugins.addons.registry.aliases.values()

SPECS = [spec for alias in ALIASES for spec in alias.test_specs]


@pytest.mark.parametrize("test_spec", SPECS)
def test_alias_test_spec(test_spec: mario.aliasing.AliasTestSpec):
    """The invocation and input generate the expected output."""

    output = subprocess.check_output(
        [sys.executable, "-m", "mario"] + test_spec.invocation,
        input=test_spec.input.encode(),
    ).decode()
    assert output == test_spec.output


@pytest.mark.parametrize("alias", ALIASES)
def test_alias_has_test(alias):
    """All aliases must have at least one test."""
    assert alias.test_specs
