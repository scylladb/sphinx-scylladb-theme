try:
    # Available in Python 3.8 and later
    import importlib.metadata as importlib_metadata
except ImportError:
    # Fallback to 'importlib_metadata' for older versions
    import importlib_metadata

version = importlib_metadata.version("sphinx-scylladb-theme")
