import click

def print_git_output(git_info: dict):
    click.secho("")
    if not git_info.get("Git Repository"):
        click.secho(f"✖ Not a git repository", fg="red", bold=True)
        click.secho(f"Reason: ", fg="yellow", nl=False)
        click.secho(f"{git_info.get('Error', 'Unknown')}", fg="white")
        click.secho("hint: Are you in root of a git repo ?", fg="yellow")
        click.secho("─" * 50, fg="bright_black")

    else:

        click.secho(f"  ✔ Git repository detected", fg="green", bold=True)

        rows = [
            ("Hidden Git File Path", git_info.get("Hidden Git File Path")),
            ("Total Contributors", git_info.get("Total Contributors", 0)),
            ("Total Commits", git_info.get("Total Commits", 0)),
            ("Last Commit Date", git_info.get("Last Commit date")),
            ("Days Since Last Commit", git_info.get("Days Since Last Commit", 0)),
        ]

        max_len = max(len(label) for label, _ in rows)

        for label, value in rows:
            click.secho(f"  {label.ljust(max_len)} : ", fg="cyan", nl=False)

            if label == "Days Since Last Commit" and isinstance(value, int):
                color = "green" if value <= 30 else "yellow" if value <= 180 else "red"
                click.secho(f"{value} days ago", fg=color, bold=True)
            else:
                click.secho(f"{value}", fg="yellow")
            click.secho("─" * 50, fg="bright_black")
    
    click.secho(" ✅ Done!\n", fg="green", bold=True)