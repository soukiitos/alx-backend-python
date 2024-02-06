#!/usr/bin/env python3
"""
Parameterize and patch as decorators
Mocking a property
Integration test: fixtures
Integration tests
"""
import unittest
import requests
from unittest.mock import patch, Mock, PropertyMock, call
from parameterized import parameterized, parameterized_class
import utils
from utils import access_nested_map, get_json, memoize
import client
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test json"""

    @parameterized.expand([
        ("google", {"google": True}),
        ("abc", {"abc": True})
        ])
    @patch('client.get_json')
    def test_org(self, org, expected, get_patch):
        '''Define test_org'''
        get_patch.return_value = expected
        self.assertEqual(GithubOrgClient(org).org, expected)
        get_patch.assert_called_once_with("https://api.github.com/orgs/"+org)

    def test_public_repos_url(self):
        """Define test_public_repos_url"""
        expected = "www.azerty.com"
        payload = {"repos_url": expected}
        to_mock = 'client.GithubOrgClient.org'
        with patch(to_mock, PropertyMock(return_value=payload)):
            cli = GithubOrgClient("x")
            self.assertEqual(cli._public_repos_url, expected)

    @patch('client.get_json')
    def test_public_repos(self, get_json_mock):
        '''Define test_public_repos'''
        violet = {"name": "violet", "license": {"key": "a"}}
        sakura = {"name": "sakura", "license": {"key": "b"}}
        kiito = {"name": "kiito"}
        expected_url = "www.azerty.com"
        get_json_mock.return_value = [violet, sakura, kiito]
        with patch(
                'client.GithubOrgClient._public_repos_url',
                new_callable=PropertyMock,
                return_value=expected_url
                ):
            x = GithubOrgClient("x")
            self.assertEqual(x.public_repos(), ['violet', 'sakura', 'kiito'])
            self.assertEqual(x.public_repos("a"), ['violet'])
            self.assertEqual(x.public_repos("c"), [])
            self.assertEqual(x.public_repos(45), [])
            get_json_mock.assert_called_once_with(expected_url)

    @parameterized.expand([
        ({'license': {'key': 'my_license'}}, 'my_license', True),
        ({'license': {'key': 'other_license'}}, 'my_license', False)
        ])
    def test_has_license(self, repo, license, expected):
        '''Define test_has_license'''
        self.assertEqual(GithubOrgClient.has_license(repo, license), expected)


@parameterized_class(
        ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
        TEST_PAYLOAD
        )
class TestIntegrationGithubOrgClient(unittest.TestCase):
    '''Test Integration'''

    
    @classmethod
    def setUpClass(cls):
        '''Define setUpclass'''
        org = TEST_PAYLOAD[0][0]
        repos = TEST_PAYLOAD[0][1]
        org_mock = Mock()
        org_mock.json = Mock(return_value=org)
        cls.org_mock = org_mock
        repos_mock = Mock()
        repos_mock.json = Mock(return_value=repos)
        cls.repos_mock = repos_mock
        cls.get_patcher = patch('requests.get')
        cls.get = cls.get_patcher.start()
        options = {org["repos_url"]: repos_mock}
        cls.get.side_effect = lambda y: options.get(y, org_mock)

    
    @classmethod
    def tearDownClass(cls):
        '''Define tearDownClass'''
        if hasattr(cls, 'get_patcher'):
            cls.get_patcher.stop()

    def test_public_repos(self):
        '''Define test_public_repos'''
        y = GithubOrgClient("x")
        self.assertEqual(y.org, self.org_payload)
        self.assertEqual(y.repos_payload, self.repos_payload)
        self.assertEqual(y.public_repos(), self.expected_repos)
        self.assertEqual(y.public_repos("NONEXISTENT"), [])
        self.get.assert_has_calls([
            call("https://api.github.com/orgs/x"),
            call(self.org_payload["repos_url"])
            ])

    def test_public_repos_with_license(self):
        '''Define test_public_repos_with_license'''
        y = GithubOrgClient("x")
        self.assertEqual(y.org, self.org_payload)
        self.assertEqual(y.repos_payload, self.repos_payload)
        self.assertEqual(y.public_repos(), self.expected_repos)
        self.assertEqual(y.public_repos("NONEXISTENT"), [])
        self.assertEqual(y.public_repos("apache-2.0"), self.apache2_repos)
        self.get.assert_has_calls([
            call("https://api.github.com/orgs/x"),
            call(self.org_payload["repos_url"])
            ])
