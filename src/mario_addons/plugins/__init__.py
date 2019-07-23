"""A plugin module for mario."""

from mario import plug


# pylint: disable=invalid-name
registry = plug.make_plugin_commands_registry("mario_addons.plugins")
