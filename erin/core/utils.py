import logging
import os
import pkgutil
from pathlib import Path
from typing import List

from erin.core.exceptions import EnvironmentVariableError, PluginNotFoundError

logger = logging.getLogger('erin')


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
    if hasattr(package, '__path__'):
        plugins = pkgutil.walk_packages(package.__path__)
    elif isinstance(package, str):
        if os.path.exists(package):
            plugins = pkgutil.walk_packages([package])
        else:
            raise PluginNotFoundError(package)
    elif isinstance(package, Path):
        if package.exists():
            plugins = pkgutil.walk_packages([package])
        else:
            raise PluginNotFoundError(package)
    else:
        raise TypeError(
            f"expected package, str, pathlib.Path or os.PathLike "
            f"object, not {type(package).__name__}"
        )

    # Create plugin import list
    plugins = [f"plugins.{i.name}" for i in plugins]
    return plugins


def config_loader(mappings, optional_envs):
    for category, settings in mappings.items():
        for setting, value in settings.items():
            if value.startswith("ENIGMA_"):
                if value in os.environ:
                    mappings[category][setting] = os.environ[value]
                elif value in optional_envs:
                    mappings[category][setting] = None
                else:
                    raise EnvironmentVariableError(
                        f"{value} is not optional.\n"
                        "Set this in your YAML file or use 'export "
                        f"{value}=YOUR_CUSTOM_VALUE' if you're a developer."
                    )
    return mappings
