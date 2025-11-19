#!/usr/bin/env python3
"""
Unit tests for the utils module.

This file contains parameterized and patched tests for the following functions:
- access_nested_map
- get_json
- memoize decorator
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize
from client import GithubOrgClient
#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient.
"""

class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient."""

    def setUp(self):
        """Start patching requests.get for each test instance."""
        self.get_patcher = patch("client.requests.get")
        self.mock_get = self.get_patcher.start()

        def get_json_side_effect(url, *args, **kwargs):
            if url.endswith("/repos"):
                return self.repos_payload
            return self.org_payload

        self.mock_get.return_value.json.side_effect = get_json_side_effect

    def tearDown(self):
        """Stop patching requests.get after each test."""
        self.get_patcher.stop()


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class."""

    # ... (previous test_org method here)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL from org."""
        org_name = "google"
        client = GithubOrgClient(org_name)
        expected_url = "https://api.github.com/orgs/google/repos"
        mock_payload = {"repos_url": expected_url}

        # Patch the org property to return our mocked payload
        with patch.object(GithubOrgClient, "org", return_value=mock_payload):
            result = client._public_repos_url
            self.assertEqual(result, expected_url)
class TestGithubOrgClient(unittest.TestCase):
    
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")  # patch get_json where it is used
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        
        # Arrange: mock return value
        expected_result = {"login": org_name}
        mock_get_json.return_value = expected_result
        
        # Act
        client = GithubOrgClient(org_name)
        result = client.org
        
        # Assert
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
"""
Unit tests for client.GithubOrgClient.
"""


class TestAccessNestedMap(unittest.TestCase):
    """Test access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns the correct value."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises KeyError for missing keys."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        # Exception message must match the missing key
        self.assertEqual(str(context.exception), f"'{path[-1]}'")


class TestGetJson(unittest.TestCase):
    """Test utils.get_json function."""

    @parameterized.expand([
        ("http://example.com",
         {"payload": True}),
        ("http://holberton.io",
         {"payload": False})
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json returns the expected payload from requests.get."""
        mock_resp = Mock()
        mock_resp.json.return_value = test_payload
        mock_get.return_value = mock_resp

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test the memoize decorator."""

    def test_memoize(self):
        """Test that a memoized property calls the method only once."""

        class TestClass:
            """Test class with a method and a memoized property."""

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()

        with patch.object(
            TestClass, "a_method", return_value=42
        ) as mock_method:
            # Call property twice; should call a_method only once
            result1 = obj.a_property
            result2 = obj.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()
