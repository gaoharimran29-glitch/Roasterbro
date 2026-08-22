import git
from typing import Any
from datetime import datetime


def humanize_timedelta(delta):
    seconds = int(delta.total_seconds())

    if seconds < 60:
        return f"{seconds} sec ago"

    minutes = seconds // 60
    if minutes < 60:
        if minutes == 1:
            return "1 min ago"
        return f"{minutes} mins ago"

    hours = minutes // 60
    if hours < 24:
        if hours == 1:
            return "1 hr ago"
        return f"{hours} hrs ago"

    days = hours // 24
    if days < 30:
        if days == 1:
            return "1 day ago"
        return f"{days} days ago"

    months = days // 30
    if months < 12:
        if months == 1:
            return "1 month ago"
        return f"{months} months ago"

    years = days // 365
    if years == 1:
        return "1 yr ago"
    return f"{years} yrs ago"


def analyze_git_repository(path: str) -> dict[str, Any]:
    """Analyze hidden git file and return git related metadata"""
    try:
        git_repo = git.Repo(path)
        git_file_path = git_repo.git_dir

        if git_repo.head.is_valid():
            commit_count = git_repo.git.rev_list("--count", "HEAD")
            last_commit = git_repo.head.commit.committed_date

            last_commit_date = datetime.fromtimestamp(last_commit)
            human_readable_date = last_commit_date.strftime(
                "%B %d, %Y, at %I:%M %p"
            )

            unique_contributors_count = len(
                git_repo.git.shortlog("-sn", "HEAD").splitlines()
            )

            today = datetime.now()
            age_diff = today - last_commit_date
            last_commit_relative = humanize_timedelta(age_diff)
        
        else:
            commit_count = 0
            last_commit_date = None
            human_readable_date = "No commits yet"
            unique_contributors_count = 0

        local_branches = git_repo.branches

        # Update remote-tracking refs and remove stale branches
        git_repo.remotes.origin.fetch(prune=True)

        remote_branches = list(git_repo.remotes.origin.refs)

        true_remote_branches = [
            branch
            for branch in remote_branches
            if not branch.name.endswith("/HEAD")
        ]

        return {
            "Git Repository": True,
            "Hidden Git File Path": git_file_path,
            "Total Contributors": unique_contributors_count,
            "Total Commits": commit_count,
            "Last Commit date": human_readable_date,
            "Last Commit": last_commit_relative,
            "Local Branches": local_branches,
            "Remote Branches": true_remote_branches,
            "No. of local branches": len(local_branches),
            "No. of remote branches": len(true_remote_branches),
        }
    
    except git.exc.InvalidGitRepositoryError:
        return {
            "Git Repository": False,
            "Error": "No git file detected"
        }
    
    except git.exc.NoSuchPathError:
        return {
            "Git Repository": False,
            "Error": "Path doesn't exists"
        }
