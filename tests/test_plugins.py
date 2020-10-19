from pathlib import Path

import pytest
from schema import SchemaError

from erin.core.exceptions import PluginNotFoundError
from erin.core.schema import plugin_schema
from erin.core.utils import find_plugins, get_plugin_data
from tests import fake_plugins


def test_find_plugins():
    """
    These tests ensure that the :meth:erin.core.utils.find_plugins`
    used for retrieving import paths is working correctly.
    """
    # Test types of paths
    plugins_list = ["fake_plugins.broken", "fake_plugins.core",
                    "fake_plugins.schema"]
    assert hasattr(fake_plugins, "__path__")
    assert find_plugins(fake_plugins) == plugins_list
    assert find_plugins("tests/fake_plugins") == plugins_list
    assert find_plugins(Path("tests/fake_plugins")) == plugins_list

    # Test exceptions
    with pytest.raises(PluginNotFoundError) as e_info:
        find_plugins("tests/incorrect_plugins_path")

    with pytest.raises(PluginNotFoundError) as e_info:
        find_plugins(Path("tests/incorrect_plugins_path"))

    with pytest.raises(TypeError) as e_info:
        find_plugins(123)


def test_get_plugin_data():
    """
    This is used to test if plugin data is imported correctly.
    """
    plugins_data_dict = {
        "tests.fake_plugins.broken": None,
        "tests.fake_plugins.core": {
            "name": "Test Core Plugins"
        },
        "tests.fake_plugins.schema": {
            "name": "Schema Plugin",
            "database": "enabled"
        },
    }

    for plugin, data in plugins_data_dict.items():
        plugin_data = get_plugin_data(plugin)
        if data:
            assert plugin_data["name"] == data["name"]
        else:
            assert plugin_data == data

        if plugin == "tests.fake_plugins.schema":
            # Ensure Schema Works
            with pytest.raises(SchemaError) as e_info:
                plugin_schema.validate(plugin_data)
