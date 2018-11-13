import importlib
import logging
import os
import pkgutil
import sys

from enigma.core.exceptions import EnvironmentVariableError

logger = logging.getLogger('enigma')


def find_extensions(package):
    """
    Finds all modules in package and presents them in the format
    required by :meth:`discord.ext.cli.Bot.load_extension`.

    This is useful when you need to load cogs from multiple
    areas of your bot. Simply convert your cogs directory
    into a package and run this method on it.

    Parameters
    -----------
    package : package
        Your extensions directory as a python package.

    Returns
    --------
    list or None
        A list of strings of format `foo.bar` as required by
        :func: `load_extension`. If package passed is not
        valid then `None` is returned instead.
    """
    loader = pkgutil.get_loader(package)
    if loader is None:
        return loader
    try:
        if not loader.is_package(package.__name__):
            return None
    except AttributeError:
        return None

    extension_list = []
    spec_list = []
    for importer, modname, ispkg in pkgutil.walk_packages(package.__path__):
        import_path = f"{package.__name__}.{modname}"
        if ispkg:
            spec = pkgutil._get_spec(importer, modname)
            importlib._bootstrap._load(spec)
            spec_list.append(spec)
        else:
            extension_list.append(import_path)

    # remove sys.modules clutter created during cog search
    for spec in spec_list:
        del sys.modules[spec.name]
    return extension_list


def find_plugins(package):
    path = package.__path__
    logger.debug(f"Package Path: {path}")


def get_extension_data(extension):
    """
    Retrieve the extension_data dictionary defined in a plugin.

    Parameters
    -----------
    extension : path to a plugin in module import format

    Returns
    --------
    dict or None
        The extension_data dict defined in a plugin or None if the
        dict is not defined.
    """
    extension = importlib.import_module(extension)
    try:
        extension_data = extension.plugin_data
    except AttributeError as e:
        extension_data = None
    finally:
        del sys.modules[extension.__name__]
        return extension_data


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
