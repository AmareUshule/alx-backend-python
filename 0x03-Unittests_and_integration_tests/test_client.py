#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient using parameterized, patch decorators,
and property mocking.
"""

import unittest
from unittest.mock import patch
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
        """Test that GithubOrgClient.org returns the correct value.

        The get_json call is patched to avoid real HTTP requests.
        """
        # Mocked return value for get_json
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        # Instantiate the client with the parameterized org name
        client = GithubOrgClient(org_name)

        # Access the org property
        result = client.org

        # Ensure get_json was called exactly once with the correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

        # Ensure the org property returns the expected payload
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL using mocked org."""
        client = GithubOrgClient("any_org")

        mock_payload = {"repos_url": "https://api.github.com/orgs/any_org/repos"}

        # Patch the 'org' property of the client instance
        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=property,
            return_value=mock_payload
        ):
            result = client._public_repos_url

        # Assert that the _public_repos_url matches the mocked payload
        self.assertEqual(result, mock_payload["repos_url"])


if __name__ == "__main__":
    unittest.main()
