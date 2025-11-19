#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient  # Make sure the client module is accessible


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods."""

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL from org."""
        org_name = "google"
        client = GithubOrgClient(org_name)
        expected_url = "https://api.github.com/orgs/google/repos"
        mock_payload = {"repos_url": expected_url}

        # Patch the org property with PropertyMock
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = mock_payload
            result = client._public_repos_url
            self.assertEqual(result, expected_url)
class TestGithubOrgClient(unittest.TestCase):
    """Test the GithubOrgClient methods."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the expected value."""
        mock_get_json.return_value = {"key": "value"}  # fake return value

        client = GithubOrgClient(org_name)
        result = client.org()  # call as method

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"key": "value"})

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL from org."""
        org_name = "google"
        client = GithubOrgClient(org_name)
        expected_url = "https://api.github.com/orgs/google/repos"
        mock_payload = {"repos_url": expected_url}

        # Patch the org property with PropertyMock
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = mock_payload
            result = client._public_repos_url
            self.assertEqual(result, expected_url)


if __name__ == "__main__":
    unittest.main()
