import click

def print_scan_output(scanning_result: dict) -> None:
    """Prints a colourful, structured summary of the scan command using click."""
    click.secho(f"📄 Files Found: ", fg="cyan", nl=False)
    click.secho(f"{len(scanning_result.get("files", 0))}", fg="yellow", bold=True)
    click.secho(f"📁 Directories Found: ", fg="cyan", nl=False)
    click.secho(f"{len(scanning_result.get("directories", 0))}", fg="yellow", bold=True)
    click.secho("📅 Created At: ", fg="cyan", nl=False)
    click.secho(f"{scanning_result.get("created_at", None)}", fg="yellow", bold=True)
    click.secho("💾 Total Size: ", fg="cyan", nl=False)
    click.secho(f"{scanning_result.get("size", 0)} MB", fg="yellow", bold=True)
    click.secho("─" * 50, fg="bright_black")

    click.secho("\n Project Important Files Checklist", fg="magenta", bold=True, underline=True)
    click.secho("")

    imp_files = scanning_result.get("imp_file", {})

    max_len = max(len(name) for name in imp_files)

    for name, present in imp_files.items():
        symbol = "✔" if present else "✖"
        color = "green" if present else "red"
        status = "Found" if present else "Missing"
        click.secho(f"  {symbol} {name.ljust(max_len)}  ", fg=color, nl=False)
        click.secho(f"{status}", fg=color, dim=not present)

    click.secho("─" * 50, fg="bright_black")

    click.secho("Suspicious Files Found: ", fg="magenta", bold=True, underline=True, nl=False)
    suspicious_files = scanning_result.get("suspicious_files", [])
    click.secho(f"{len(suspicious_files)}", fg="yellow", bold=True)

    if not suspicious_files:
        click.secho("  ✔ No suspicious files found", fg="green")
    else:
        for f in suspicious_files:
            click.secho(f"  ⚠ {f}", fg="red", bold=True)

    click.secho("─" * 50, fg="bright_black")
