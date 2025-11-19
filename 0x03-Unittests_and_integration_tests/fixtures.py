#!/usr/bin/env python3
"""
Fixtures for GithubOrgClient integration tests.
"""

org_payload = {
    "login": "google",
    "id": 123,
    "repos_url": "https://api.github.com/orgs/google/repos"
}

repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2"}},
    {"name": "repo2", "license": {"key": "mit"}}
]

expected_repos = ["repo1", "repo2"]
apache2_repos = ["repo1"]
