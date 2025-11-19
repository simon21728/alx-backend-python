#!/usr/bin/env python3
"""
Module for GithubOrgClient.
"""

import requests


def get_json(url):
    """Fetch JSON payload from a URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


class GithubOrgClient:
    """A client for interacting with the GitHub organization API."""

    def __init__(self, org_name):
        self.org_name = org_name

    def org(self):
        """Return the JSON payload of the organization."""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)
