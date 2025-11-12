#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient using parameterized, patch decorators,
property mocking, and more advanced patching.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
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

        self.assertEqual(result, mock_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repo names."""

        client = GithubOrgClient("any_org")

        # Payload returned by the mocked get_json
        mocked_repos_payload = [
            {"name": "repo1", "license": {"key": "MIT"}},
            {"name": "repo2", "license": {"key": "GPL"}},
            {"name": "repo3"}  # No license key
        ]
        mock_get_json.return_value = mocked_repos_payload

        # Patch the _public_repos_url property with line split for PEP8
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=property,
            return_value=(
                "https://api.github.com/orgs/any_org/repos"
            )
        ) as mock_url_prop:
            result = client.public_repos()

        # Ensure the list of repos returned matches the mocked payload
        expected_repo_names = ["repo1", "repo2", "repo3"]
        self.assertEqual(result, expected_repo_names)

        # Assert the mocked property and get_json were called once
        mock_get_json.assert_called_once()
        self.assertEqual(mock_url_prop.call_count, 1)


if __name__ == "__main__":
    unittest.main()
