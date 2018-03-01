import importlib
import pkgutil
import sys


def find_cogs(package):
    """
    Finds all modules in package and presents them in the format
    required by :meth:`discord.ext.commands.Bot.load_extension`.

    This is useful when you need to load cogs from multiple
    areas of your bot. Simply convert your cogs directory
    into a package and run this method on it.

    Parameters
    -----------
    package : package
        Your cogs directory as a python package.

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

    cog_list = []
    spec_list = []
    for importer, modname, ispkg in pkgutil.walk_packages(package.__path__):
        import_path = f"{package.__name__}.{modname}"
        if ispkg:
            spec = pkgutil._get_spec(importer, modname)
            importlib._bootstrap._load(spec)
            spec_list.append(spec)
        else:
            cog_list.append(import_path)

    # remove sys.modules clutter created during cog search
    for spec in spec_list:
        del sys.modules[spec.name]
    return cog_list
