import click

def print_whitespace_output(results: dict[str, list[int]]) -> None:
    """Prints a colourful, structured summary of the whitespace scan using click."""
    if not results:
        click.echo(click.style("\n✨ Success: No trailing whitespaces found in any files!", fg="green", bold=True))
        return

    click.echo(click.style(f"\n⚠️  Found issues in {len(results)} file(s):\n", fg="yellow", bold=True))

    for file_path, line_numbers in results.items():
        click.echo(click.style(f"📄 {file_path}", fg="cyan", bold=True))
        lines_str = ", ".join(map(str, line_numbers))
        click.echo(click.style("   ↳ Trailing whitespace on lines: ", fg="green") + click.style(lines_str, fg="red"))

    click.secho("")
