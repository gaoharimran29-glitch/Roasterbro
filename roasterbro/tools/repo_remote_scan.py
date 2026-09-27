"""Orchestrates scanning a remote GitHub repository: fetch metadata via the
API, download a snapshot via the tarball endpoint, then run the existing
local scanning pipeline against the extracted contents unchanged."""

import tarfile
import tempfile
from pathlib import Path
from typing import Any
from datetime import datetime, timezone

import click

from roasterbro.utils import github_api
from roasterbro.tools.repo_basic_scan import repo_scan_findings
from roasterbro.tools.repo_deps_scan import dependencies_analyzer
from roasterbro.tools.repo_file_scan import file_metrics
from roasterbro.tools.repo_lang_scan import languages_present


def _build_remote_git_info(owner: str, repo: str, default_branch: str, token: str | None) -> dict[str, Any]:
    """Same dict shape as tools.repo_git_scan.analyze_git_repository, so the
    existing git_output_formatter.print_git_output works completely unchanged."""
    commit_count = github_api.get_commit_count(owner, repo, ref=default_branch, token=token)
    contributor_count = github_api.get_contributor_count(owner, repo, token=token)
    remote_branches = github_api.get_branches(owner, repo, token=token)
    latest_commit = github_api.get_latest_commit(owner, repo, ref=default_branch, token=token)

    if latest_commit:
        committed_at = latest_commit["commit"]["committer"]["date"]
        last_commit_date = datetime.fromisoformat(
            committed_at.replace("Z", "+00:00")
        )
        human_readable_date = last_commit_date.strftime("%B %d, %Y, at %I:%M %p")
        age_diff = datetime.now(timezone.utc) - last_commit_date
        last_commit_relative = _humanize_timedelta(age_diff)
    else:
        human_readable_date = "No commits yet"
        last_commit_relative = None

    return {
        "Git Repository": True,
        "Hidden Git File Path": f"(remote) github.com/{owner}/{repo}",
        "Total Contributors": contributor_count,
        "Total Commits": commit_count,
        "Last Commit date": human_readable_date,
        "Last Commit": last_commit_relative,
        "Local Branches": [],
        "Remote Branches": remote_branches,
        "No. of local branches": 0,
        "No. of remote branches": len(remote_branches),
    }


def _humanize_timedelta(delta):
    seconds = int(delta.total_seconds())
    if seconds < 60:
        return f"{seconds} sec ago"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes} min ago" if minutes == 1 else f"{minutes} mins ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} hr ago" if hours == 1 else f"{hours} hrs ago"
    days = hours // 24
    if days < 30:
        return f"{days} day ago" if days == 1 else f"{days} days ago"
    months = days // 30
    if months < 12:
        return f"{months} month ago" if months == 1 else f"{months} months ago"
    years = days // 365
    return f"{years} yr ago" if years == 1 else f"{years} yrs ago"


def _extract_tarball(tarball_path: str, dest_dir: str) -> Path:
    """GitHub tarballs extract into a single top-level dir named like
    'owner-repo-<sha>' — find and return it."""
    with tarfile.open(tarball_path, "r:gz") as tar:
        tar.extractall(dest_dir, filter="data")
    extracted = [p for p in Path(dest_dir).iterdir() if p.is_dir()]
    if not extracted:
        raise RuntimeError("Tarball extraction produced no directory — download may be corrupt.")
    return extracted[0]


def remote_scan_findings(target: str, ref: str | None = None, token: str | None = None) -> dict[str, Any]:
    """Full scan of a remote GitHub repo. Mirrors repo_roast_scan.full_scan_for_roast's
    output shape, plus a bonus 'GitHub Metadata' section only the API can provide."""
    owner, repo = github_api.parse_github_target(target)

    click.secho(f"\n🌐 Fetching metadata for {owner}/{repo} from the GitHub API...", fg="yellow")
    metadata = github_api.get_repo_metadata(owner, repo, token=token)
    resolved_ref = ref or metadata["default_branch"]

    with tempfile.TemporaryDirectory(prefix="roasterbro-remote-") as tmp:
        tarball_path = str(Path(tmp) / "repo.tar.gz")

        click.secho(f"📥 Downloading snapshot ({resolved_ref})...", fg="yellow")
        github_api.download_tarball(owner, repo, tarball_path, ref=resolved_ref, token=token)

        extract_dir = Path(tmp) / "extracted"
        extract_dir.mkdir()
        repo_root = _extract_tarball(tarball_path, str(extract_dir))

        click.secho("🔍 Running scan against downloaded snapshot...\n", fg="yellow")

        scanning_result = repo_scan_findings(repo_root)
        scanning_result["created_at"] = metadata["created_at"]
        scanning_result["created_at_is_exact"] = True
        files = scanning_result.get("files", [])
        languages = languages_present(files=files)
        dep = dependencies_analyzer(files=files)

        directories = scanning_result.get("directories", [])
        has_test = scanning_result.get("has_test", False)
        stats = file_metrics(files=files, has_test=has_test, directories=directories)

        git_info = _build_remote_git_info(owner, repo, resolved_ref, token)

        return {
            "GitHub Metadata": metadata,
            "Repo Info": scanning_result,
            "Languages": languages,
            "GitHub-Reported Languages (bytes)": github_api.get_languages(owner, repo, token=token),
            "Dependencies": dep,
            "File Stats": stats,
            "Git Info": git_info,
        }
