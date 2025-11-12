#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the expected dictionary."""
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_repos_payload(self, org_name, mock_get_json):
        """Test that repos_payload returns expected list of repos."""
        expected_org_payload = {"repos_url": f"https://api.github.com/orgs/{org_name}/repos"}
        expected_repos_payload = [{"name": "repo1"}, {"name": "repo2"}]

        # Mock org() first
        mock_get_json.side_effect = [expected_org_payload, expected_repos_payload]

        client = GithubOrgClient(org_name)
        result = client.repos_payload

        # First call should fetch the repos_url from org
        self.assertEqual(result, expected_repos_payload)
        self.assertEqual(mock_get_json.call_count, 2)

    @parameterized.expand([
        ({"license": {"key": "MIT"}}, "MIT", True),
        ({"license": {"key": "GPL"}}, "MIT", False),
        ({}, "MIT", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license static method."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)

