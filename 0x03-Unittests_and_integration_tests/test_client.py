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
        """Test that GithubOrgClient.org returns the correct value."""
        # Setup mock return value
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        # Instantiate GithubOrgClient with the parameterized org
        client = GithubOrgClient(org_name)

        # Call the org property
        result = client.org

        # Assert get_json called exactly once with the correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

        # Assert the org property returns the expected payload
        self.assertEqual(result, expected_payload)

