import importlib
import logging
import os
import pkgutil
import sys
from pathlib import Path
from typing import List

from erin.core.exceptions import EnvironmentVariableError, PluginNotFoundError

logger = logging.getLogger(__name__)


def find_plugins(package) -> List[str]:
    """
    Finds all top level subpackages in a package and presents them in
    the format required by :meth:`discord.ext.cli.Bot.load_extension`.

    This is useful when you need to load cogs from multiple
    areas of your bot. Simply convert your cogs directory
    into a package and run this method on it.

    Parameters
    -----------
    package : package
        Your package as a python package or a path to one.
        Note: All packages are modules, all modules are not packages.

    Returns
    --------
    list or None
        A list of strings of format `foo.bar` as required by
        :meth:`discord.ext.cli.Bot.load_extension`. If package passed is not
        valid then `None` is returned instead.
    """
    # Check if parameter is a package
    if hasattr(package, "__path__"):
        plugins = pkgutil.walk_packages(package.__path__)
        package_name = os.path.basename(package.__path__[0])
    elif isinstance(package, str):
        if os.path.exists(package):
            plugins = pkgutil.walk_packages([package])
            package_name = os.path.basename(package)
        else:
            raise PluginNotFoundError(package)
    elif isinstance(package, Path):
        if package.exists():
            plugins = pkgutil.walk_packages([package])
            package_name = os.path.basename(str(package))
        else:
            raise PluginNotFoundError(package)
    else:
        raise TypeError(
            f"expected package, str, pathlib.Path or os.PathLike "
            f"object, not {type(package).__name__}"
        )

    # Create plugin import list
    plugins = [f"{package_name}.{i.name}" for i in plugins]
    return plugins


def get_plugin_data(plugin):
    """
    Retrieve the plugin_data dictionary defined in a plugin.
    Parameters
    -----------
    plugin : path to a plugin in module import format
    Returns
    --------
    dict or None
        The plugin_data dict defined in a plugin or None if the dict is
        not defined.
    """
    logger.debug(f"Attempting Plugin Import: {plugin}")
    plugin = importlib.import_module(plugin)
    plugin_data = None
    try:
        plugin_data = plugin.plugin_data
    except AttributeError:
        plugin_data = None
    finally:
        del sys.modules[plugin.__name__]
        return plugin_data


def config_loader(mappings, optional_envs):
    for category, settings in mappings.items():
        for setting, value in settings.items():
            if value.startswith("ERIN_"):
                if value in os.environ:
                    mappings[category][setting] = os.environ[value]
                elif value in optional_envs:
                    mappings[category][setting] = None
                else:
                    raise EnvironmentVariableError(
                        f"{value} is not optional.\n"
                        "Set this in your TOML config file or use 'export "
                        f"{value}=YOUR_CUSTOM_VALUE'!"
                    )
    return mappings
