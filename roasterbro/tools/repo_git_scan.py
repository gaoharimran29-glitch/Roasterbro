import git
from typing import Any
from datetime import datetime


def analyze_git_repository(path: str) -> dict[str, Any]:
    """Analyze hidden git file and return git related metadata"""
    try:
        git_repo = git.Repo(path, search_parent_directories=True)
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
            days_ago = age_diff.days
        else:
            commit_count = 0
            last_commit_date = None
            human_readable_date = "No commits yet"
            unique_contributors_count = 0
            days_ago = None

        local_branches = git_repo.branches
        remote_branches = [
            ref
            for remote in git_repo.remotes
            for ref in remote.refs
        ]
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
            "Days Since Last Commit": days_ago,
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
