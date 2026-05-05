from importlib.metadata import version

try:
    __package_name__ = 'seerapi-solaris'
    __version__ = version(__package_name__)
except Exception:
    __version__ = None
