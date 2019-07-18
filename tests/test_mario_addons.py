import subprocess
import sys

import mario.aliasing
import pytest

import mario_addons.plugins.addons


SPECS = [
    spec
    for alias in mario_addons.plugins.addons.registry.aliases.values()
    for spec in alias.test_specs
]


@pytest.mark.parametrize("test_spec", SPECS)
def test_alias_test_spec(test_spec: mario.aliasing.AliasTestSpec):

    output = subprocess.check_output(
        [sys.executable, "-m", "mario"] + test_spec.invocation,
        input=test_spec.input.encode(),
    ).decode()
    assert output == test_spec.output
