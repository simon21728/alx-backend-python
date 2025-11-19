#!/usr/bin/env python3
"""
Utility functions for testing lessons.
"""

import requests
from functools import wraps
from typing import Mapping, Any, Sequence


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Access a nested map using a sequence of keys.
    """
    current = nested_map
    for key in path:
        current = current[key]
    return current


def get_json(url: str) -> Any:
    """
    Make a GET request to a URL and return the JSON response.
    """
    response = requests.get(url)
    return response.json()


def memoize(method):
    """
    Decorator to cache the result of a method.
    """

    @wraps(method)
    def wrapper(self):
        attr = f"_{method.__name__}"
        if not hasattr(self, attr):
            setattr(self, attr, method(self))
        return getattr(self, attr)

    return wrapper
