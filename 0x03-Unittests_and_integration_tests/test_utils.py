#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch, Mock
from utils import get_json
from unittest.mock import patch
from utils import memoize
#!/usr/bin/env python3

class TestMemoize(unittest.TestCase):
    """Test the memoize decorator."""

    def test_memoize(self):
        """Test that a memoized property calls the method only once."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            # Call property twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Check return value
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Ensure a_method was called only once
            mock_method.assert_called_once()

class TestGetJson(unittest.TestCase):
    """Test utils.get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
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

class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{path[-1]}'")
