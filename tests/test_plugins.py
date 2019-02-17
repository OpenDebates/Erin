from pathlib import Path

from tests import fake_plugins

import pytest
from glia.core.exceptions import PluginNotFoundError
from glia.core.utils import find_plugins, get_plugin_data


def test_find_plugins():
    """
    These tests ensure that the :meth:glia.core.utils.find_plugins`
    used for retrieving import paths is working correctly.
    """

    # Test types of paths
    plugins_list = [
        'fake_plugins.core'
    ]
    assert hasattr(fake_plugins, '__path__')
    assert find_plugins(fake_plugins) == plugins_list
    assert find_plugins('tests/fake_plugins') == plugins_list
    assert find_plugins(Path('tests/fake_plugins')) == plugins_list

    # Test exceptions
    with pytest.raises(PluginNotFoundError) as e_info:
        find_plugins('tests/incorrect_plugins_path')

    with pytest.raises(PluginNotFoundError) as e_info:
        find_plugins(Path('tests/incorrect_plugins_path'))

    with pytest.raises(TypeError) as e_info:
        find_plugins(123)


def test_get_plugin_data():
    """
    This is used to test if plugin data is imported correctly.
    """
    plugins_data_dict = {
        'fake_plugins.core': {
            "name": "Test Core Plugins"
        }
    }
    for plugin, data in plugins_data_dict.items():
        assert get_plugin_data(plugin)["name"] == data["name"]
