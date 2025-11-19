#!/usr/bin/env python3
"""
Utils module
"""

from typing import Any, Mapping, Sequence
import requests


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Access a nested map with a sequence of keys.
    """
    value = nested_map
    for key in path:
        value = value[key]
    return value


def get_json(url: str) -> Any:
    """
    Get JSON from URL using requests
    """
    response = requests.get(url)
    return response.json()


class memoize:
    """
    Decorator class to memoize methods
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype):
        """
        Turns the method into a property-like cached attribute.
        """
        if obj is None:
            return self
        attr_name = self.func.__name__
        if not hasattr(obj, attr_name):
            setattr(obj, attr_name, self.func(obj))
        return getattr(obj, attr_name)
