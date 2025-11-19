#!/usr/bin/env python3
"""
Utility functions for various tasks:
- access_nested_map
- get_json
- memoize decorator
"""

from functools import wraps
import requests


def access_nested_map(nested_map, path):
    """Access a nested map using a sequence of keys."""
    current = nested_map
    for key in path:
        current = current[key]
    return current


def get_json(url):
    """Get JSON content from a URL."""
    response = requests.get(url)
    return response.json()


def memoize(fn):
    """Memoize a method's return value."""
    attr_name = "_memoized_" + fn.__name__

    @property
    @wraps(fn)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return wrapper
