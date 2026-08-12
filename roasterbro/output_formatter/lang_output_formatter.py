import click

def print_lang_output(languages: dict) -> None:
    """Prints a colourful, structured summary of the langs command using click."""
    click.secho("💻 Languages Detected", fg="magenta", bold=True, underline=True)
    
    if not languages:
        click.secho("✖ No recognized languages found", fg="red")
        click.secho("─" * 50, fg="bright_black")
        return

    total = sum(languages.values())
    sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
    max_len = max(len(lang) for lang, _ in sorted_langs)

    colors = ["green", "cyan", "yellow", "blue", "magenta", "white"]

    for i, (lang, count) in enumerate(sorted_langs):
        percent = (count / total) * 100
        bar_len = int(percent / 5)
        bar = "█" * bar_len
        color = colors[i % len(colors)]

        click.secho(f"  {lang.ljust(max_len)} : ", fg="cyan", nl=False)
        click.secho(f"{str(count).rjust(3)} files  ", fg="yellow", nl=False)
        click.secho(f"{bar} ", fg=color, nl=False)
        click.secho(f"{percent:.1f}%", fg="bright_black")

    click.secho("─" * 50, fg="bright_black")
    click.secho(f"  Total: ", fg="cyan", nl=False)
    click.secho(f"{total} files across {len(languages)} language(s)", fg="green", bold=True)
    click.secho("─" * 50, fg="bright_black")
