import click

def print_roast(text: str):
    width = 70
    click.echo()
    click.secho("╔" + "═" * width + "╗", fg="red")
    click.secho("║" + " 🔥 REPO ROAST ".center(width) + "║", fg="red", bold=True)
    click.secho("╚" + "═" * width + "╝", fg="red")
    click.echo()
    for line in text.split("\n"):
        click.secho(line, fg="white")
    click.echo()
    click.secho("─" * width, fg="red")  # fixed: matches question box width now
    click.echo()

def print_question(text: str):
    width = 70
    text = text.strip()
    click.echo()
    click.secho("┌" + "─" * width + "┐", fg="cyan")
    click.secho("│" + " 🤔 ONE MORE THING... ".center(width) + "│", fg="cyan", bold=True)
    click.secho("└" + "─" * width + "┘", fg="cyan")
    click.echo()
    for line in text.split("\n"):
        click.secho(line, fg="bright_cyan")
    click.echo()