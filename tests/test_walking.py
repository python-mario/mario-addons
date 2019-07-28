import pytest

from mario_addons.plugins import walking


@pytest.mark.parametrize("name", ["collections.OrderedDict", "int"])
def test_get_type_object(name):
    result = walking.get_type_object(name)
    assert isinstance(result, type)

    expected_name = result.__module__ + "." + result.__qualname__
    if expected_name.startswith("builtins."):
        expected_name = expected_name[len("builtins.") :]
    assert expected_name == name
