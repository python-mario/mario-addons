import subprocess
import sys

import mario.declarative
import pytest

import mario_addons.plugins.addons


ALIASES = mario_addons.plugins.addons.registry.commands.values()

SPECS = [spec for command in ALIASES for spec in command.test_specs]


@pytest.mark.parametrize("test_spec", SPECS)
def test_command_test_spec(test_spec: mario.declarative.CommandTestSpec):
    """The invocation and input generate the expected output."""

    output = subprocess.check_output(
        [sys.executable, "-m", "mario"] + test_spec.invocation,
        input=test_spec.input.encode(),
    ).decode()
    assert output == test_spec.output


@pytest.mark.parametrize("command", ALIASES)
def test_command_has_test(command):
    """All commands must have at least one test."""
    assert command.test_specs
