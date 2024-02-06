#!/usr/bin/env python3
'''Parameterize a unit test and Mock HTTP calls'''

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    '''Inherits from unittest.TestCase'''
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        '''Define test_access_nested_map'''
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",), {'a'}),
        ({"a": 1}, ("a", "b"), {'b'})
        ])
    def test_access_nested_map_exception(
            self, nested_map, path, expected_exception
            ):
        '''Define test_access_nested_map_exception'''
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
            self.assertEqual(expected_exception, e.exception)


class TestGetJson(unittest.TestCase):
    '''Class TestGetJson to mock HTTP calls'''

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
        ])
    def test_get_json(self, test_url, test_payload):
        '''Define test_get_json'''
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        with patch('requests.get', return_value=mock_response):
            res = get_json(test_url)
            self.assertEqual(res, test_payload)
            mock_response.json.assert_called_once()


class TestMemoize(unittest.TestCase):
    """Class TestMemoize to Parameterize and patch"""

    def test_memoize(self):
        '''Define test_memoize'''

        class TestClass:
            """Parameterize and patch"""

            def a_method(self):
                '''Define a_method'''
                return 42

            @memoize
            def a_property(self):
                '''Define a_property'''
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as patched:
            test_class = TestClass()
            re_return = test_class.a_property
            re_return = test_class.a_property

            self.assertEqual(re_return, 42)
            patched.assert_called_once()
