import click

def print_git_output(git_info: dict):
    click.secho("")
    if not git_info.get("Git Repository"):
        click.secho(f"✖ Not a git repository", fg="red", bold=True)
        click.secho(f"Reason: ", fg="yellow", nl=False)
        click.secho(f"{git_info.get('Error', 'Unknown')}", fg="white")
        click.secho("hint: Are you in root of a git repo ?", fg="yellow")
        click.secho("─" * 50, fg="bright_black")
        click.secho(" ✨ Done!\n", fg="green", bold=True)
        return

    click.secho(f"  ✔ Git repository detected", fg="green", bold=True)
    click.secho("─" * 50, fg="bright_black")
    
    metadata_rows = [
        ("Hidden Git File Path", git_info.get("Hidden Git File Path")),
        ("Total Contributors", git_info.get("Total Contributors", 0)),
        ("Total Commits", git_info.get("Total Commits", 0)),
        ("Last Commit Date", git_info.get("Last Commit date")),
        ("Days Since Last Commit", git_info.get("Days Since Last Commit", 0)),
    ]

    max_len = max(len(label) for label, _ in metadata_rows)
    branch_label_len = max(max_len, len("Remote Branches (999)"))

    for label, value in metadata_rows:
        click.secho(f"  {label.ljust(branch_label_len)} : ", fg="cyan", nl=False)

        if label == "Days Since Last Commit" and isinstance(value, int):
            color = "green" if value <= 30 else "yellow" if value <= 180 else "red"
            click.secho(f"{value} days ago", fg=color, bold=True)
        else:
            click.secho(f"{value}", fg="yellow")
        click.secho("─" * 50, fg="bright_black")

    local_branches = git_info.get("Local Branches", [])
    local_count = git_info.get("No. of local branches", len(local_branches) if isinstance(local_branches, list) else 0)
    
    click.secho(f"  {'Local Branches'.ljust(branch_label_len)} : ", fg="cyan", nl=False)
    click.secho(f"({local_count})", fg="yellow", bold=True)
    
    if isinstance(local_branches, list):
        for branch in local_branches:
            click.secho(f"    • {branch}", fg="green", bold=True)
    click.secho("─" * 50, fg="bright_black")

    remote_branches = git_info.get("Remote Branches", [])
    remote_count = git_info.get("No. of remote branches", len(remote_branches) if isinstance(remote_branches, list) else 0)
    
    click.secho(f"  {'Remote Branches'.ljust(branch_label_len)} : ", fg="cyan", nl=False)
    click.secho(f"({remote_count})", fg="yellow", bold=True)
    
    if isinstance(remote_branches, list):
        for branch in remote_branches:
            click.secho(f"    • {branch}", fg="green", bold=True)
    click.secho("─" * 50, fg="bright_black")
