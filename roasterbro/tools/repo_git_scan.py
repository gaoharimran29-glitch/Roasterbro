from datetime import datetime
import git

def analyze_git_repository(path: str) -> dict:
    """Analyze hidden git file and return git related metadata"""
    try:
        git_repo = git.Repo(path, search_parent_directories=True)
        git_file_path = git_repo.git_dir
        commit_count = git_repo.git.rev_list('--count' , 'HEAD')
        last_commit = git_repo.head.commit.committed_date
        last_commit_date = datetime.fromtimestamp(last_commit)
        human_readable_date = last_commit_date.strftime("%B %d, %Y, at %I:%M %p")
        unique_contributors_count = len(git_repo.git.shortlog("-sn", "HEAD").splitlines())

        today = datetime.now()
        age_diff = today - last_commit_date
        days_ago = age_diff.days

        return {
            "Git Repository": True,
            "Hidden Git File Path": git_file_path,
            "Total Contributors": unique_contributors_count,
            "Total Commits": commit_count,
            "Last Commit date": human_readable_date,
            "Days Since Last Commit": days_ago
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