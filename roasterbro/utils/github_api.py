"""Thin client around the GitHub REST API for remote repository scanning."""

import os
import re
import requests

API_BASE = "https://api.github.com"


class GitHubAPIError(Exception):
    """Base error for GitHub API failures."""


class RepoNotFoundError(GitHubAPIError):
    """Raised when the repo doesn't exist or isn't accessible with the given token."""


class RateLimitError(GitHubAPIError):
    """Raised when the GitHub API rate limit has been exhausted."""


def _headers(token: str | None) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = token or os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _request(method: str, url: str, token: str | None, **kwargs) -> requests.Response:
    resp = requests.request(method, url, headers=_headers(token), timeout=30, **kwargs)

    if resp.status_code == 404:
        raise RepoNotFoundError(
            "Repository not found (or private and no valid GITHUB_TOKEN was provided)."
        )

    if resp.status_code == 403 and resp.headers.get("X-RateLimit-Remaining") == "0":
        reset = resp.headers.get("X-RateLimit-Reset")
        raise RateLimitError(
            f"GitHub API rate limit exceeded. Resets at epoch {reset}. "
            "Set a GITHUB_TOKEN environment variable to raise your limit from 60/hr to 5,000/hr."
        )

    resp.raise_for_status()
    return resp


def parse_github_target(target: str) -> tuple[str, str]:
    """Parse 'owner/repo', a full GitHub URL, or an SSH URL into (owner, repo)."""
    target = target.strip().rstrip("/")

    patterns = [
        r"^https?://github\.com/([^/]+)/([^/]+?)(\.git)?$",
        r"^git@github\.com:([^/]+)/([^/]+?)(\.git)?$",
        r"^([^/]+)/([^/]+)$",  # bare "owner/repo" shorthand
    ]
    for pattern in patterns:
        m = re.match(pattern, target)
        if m:
            return m.group(1), m.group(2)

    raise ValueError(
        f"Couldn't parse '{target}' as a GitHub repo. "
        "Use 'owner/repo', a GitHub URL, or an SSH URL."
    )


def get_repo_metadata(owner: str, repo: str, token: str | None = None) -> dict:
    """GET /repos/{owner}/{repo} — basic repo info, including the default branch."""
    resp = _request("GET", f"{API_BASE}/repos/{owner}/{repo}", token)
    data = resp.json()
    return {
        "full_name": data.get("full_name"),
        "description": data.get("description"),
        "created_at": data.get("created_at"),
        "default_branch": data.get("default_branch"),
        "stargazers_count": data.get("stargazers_count"),
        "forks_count": data.get("forks_count"),
        "open_issues_count": data.get("open_issues_count"),
        "size_kb": data.get("size"),
        "private": data.get("private"),
        "archived": data.get("archived"),
    }


def _count_via_link_header(resp: requests.Response, fallback_body: list) -> int:
    """GitHub doesn't return a total count for paginated endpoints. Trick: request
    per_page=1 and read the page number out of the 'last' rel in the Link header —
    that number IS the total count, without paginating through everything."""
    link = resp.headers.get("Link", "")
    match = re.search(r'[?&]page=(\d+)>;\s*rel="last"', link)
    if match:
        return int(match.group(1))
    # No Link header means everything fit on one page.
    return len(fallback_body)


def get_commit_count(owner: str, repo: str, ref: str | None = None, token: str | None = None) -> int:
    """Total commit count on a branch, via the per_page=1 + Link header trick."""
    params = {"per_page": 1}
    if ref:
        params["sha"] = ref
    resp = _request("GET", f"{API_BASE}/repos/{owner}/{repo}/commits", token, params=params)
    return _count_via_link_header(resp, resp.json())


def get_latest_commit(owner: str, repo: str, ref: str | None = None, token: str | None = None) -> dict | None:
    """Return the latest commit on a branch, including its author date."""
    params = {"per_page": 1}
    if ref:
        params["sha"] = ref
    resp = _request("GET", f"{API_BASE}/repos/{owner}/{repo}/commits", token, params=params)
    commits = resp.json()
    return commits[0] if commits else None


def get_contributor_count(owner: str, repo: str, token: str | None = None) -> int:
    resp = _request(
        "GET", f"{API_BASE}/repos/{owner}/{repo}/contributors", token,
        params={"per_page": 1, "anon": "false"},
    )
    return _count_via_link_header(resp, resp.json())


def get_branches(owner: str, repo: str, token: str | None = None) -> list[str]:
    branches, page = [], 1
    while True:
        resp = _request(
            "GET", f"{API_BASE}/repos/{owner}/{repo}/branches", token,
            params={"per_page": 100, "page": page},
        )
        batch = resp.json()
        if not batch:
            break
        branches.extend(b["name"] for b in batch)
        page += 1
    return branches


def get_languages(owner: str, repo: str, token: str | None = None) -> dict[str, int]:
    """GitHub's own byte-count-per-language breakdown — a nice cross-check
    against RoasterBro's own extension-based detection."""
    resp = _request("GET", f"{API_BASE}/repos/{owner}/{repo}/languages", token)
    return resp.json()


def download_tarball(owner: str, repo: str, dest_path: str, ref: str | None = None, token: str | None = None) -> None:
    """GET /repos/{owner}/{repo}/tarball/{ref} — one call, full repo snapshot."""
    url = f"{API_BASE}/repos/{owner}/{repo}/tarball"
    if ref:
        url += f"/{ref}"

    resp = _request("GET", url, token, stream=True, allow_redirects=True)
    with open(dest_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
