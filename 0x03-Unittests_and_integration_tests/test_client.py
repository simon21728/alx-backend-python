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

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repo names."""
        org_name = "google"
        client = GithubOrgClient(org_name)

        # Mock _public_repos_url property
        expected_url = "https://api.github.com/orgs/google/repos"
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_repos_url:

            mock_repos_url.return_value = expected_url

            # Mock get_json to return a list of repos
            repo_payload = [
                {"name": "repo1", "license": {"key": "mit"}},
                {"name": "repo2", "license": {"key": "apache-2.0"}}
            ]
            mock_get_json.return_value = repo_payload

            result = client.public_repos()

            # Check the output
            self.assertEqual(result, ["repo1", "repo2"])

            # Check that mocks were called once
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(expected_url)
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
