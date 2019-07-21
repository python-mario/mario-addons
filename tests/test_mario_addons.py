import itertools
import subprocess
import sys

import attr
import mario.declarative
import pytest

import mario_addons.plugins.addons


COMMANDS = mario_addons.plugins.addons.registry.commands.values()
TEST_SPECS = [test_spec for command in COMMANDS for test_spec in command.tests]
REQUIRED_FIELDS = ["tests", "help", "short_help"]


def get_param_id(param):
    if attr.has(type(param)):
        return repr(attr.asdict(param))
    return repr(param)


@pytest.mark.parametrize("test_spec", TEST_SPECS, ids=get_param_id)
def test_command_test_spec(test_spec: mario.declarative.CommandTest):
    """The invocation and input generate the expected output."""

    output = subprocess.check_output(
        [sys.executable, "-m", "mario"] + test_spec.invocation,
        input=test_spec.input.encode(),
    ).decode()
    assert output == test_spec.output


@pytest.mark.parametrize("command", COMMANDS, ids=get_param_id)
@pytest.mark.parametrize("field_name", REQUIRED_FIELDS, ids=get_param_id)
def test_command_has_required_fields(command, field_name):
    attribute = getattr(command, field_name)
    assert attribute
