#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized,parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
from utils import get_json


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get and configure side_effect."""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        def get_json_side_effect(url, *args, **kwargs):
            """Return correct fixture based on URL."""
            if url.endswith("/repos"):
                return cls.repos_payload
            return cls.org_payload

        cls.mock_get.return_value.json.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected list of repository names."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filtering by license (apache-2)."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2"), self.apache2_repos)



class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient."""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns expected boolean based on license key."""
        client = GithubOrgClient("org_name")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)



class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org returns expected data."""
        mock_get_json.return_value = {"payload": True}

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"payload": True})

    def test_public_repos_url(self):
        """Test that _public_repos_url returns repos_url from org."""
        expected_url = "https://api.github.com/orgs/google/repos"
        mock_payload = {"repos_url": expected_url}

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
            return_value=mock_payload
        ):
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list of repo names."""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value="http://example.com"
        ):
            client = GithubOrgClient("google")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("http://example.com")
