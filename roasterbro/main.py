from roasterbro.scanner import repo_scan_findings, analyze_git_repository, languages_present
from roasterbro.analyzer import analyze_repo
from roasterbro.utils import scan_and_validate
from pathlib import Path
import click

BANNER = r"""
╭────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                        │
│                      _____                 _            _                                              │
│                     |  __ \               | |          | |                                             │
│                     | |__) |___   __ _ ___| |_ ___ _ __| |__  _ __ ___                                 │
│                     |  _  // _ \ / _` / __| __/ _ \ '__| '_ \| '__/ _ \                                │
│                     | | \ \ (_) | (_| \__ \ ||  __/ |  | |_) | | | (_) |                               │
│                     |_|  \_\___/ \__,_|___/\__\___|_|  |_.__/|_|  \___/                                │
│                                                                                                        │
│                             A CLI to roast your codebase - 0.1.0                                       │
│                                     Made by - Gaohar Imran                                             │
│                                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────╯
"""

@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option("0.1.0", "-v", "--version", prog_name="Roasterbro", message="%(prog)s %(version)s")
@click.pass_context
def main(ctx):
    """RoasterBro - A CLI to roast your codebase."""
    if ctx.invoked_subcommand is None:
        click.secho(BANNER, fg="green", bold=True)
        click.echo(ctx.get_help())

@main.command()
@click.argument("path", required=False, default=None)
def scan(path):
    cwd = scan_and_validate(path)

    click.secho("")
    click.secho("─" * 50, fg="bright_black")
    click.secho(f"📂 Scanning: ", fg="cyan", bold=True, nl=False)
    click.secho(f"{cwd}", fg="white")

    scanning_result = repo_scan_findings(cwd)

    click.secho(f"📄 Files Found: ", fg="cyan", nl=False)
    click.secho(f"{len(scanning_result.get("files", 0))}", fg="yellow", bold=True)
    click.secho(f"📁 Directories Found: ", fg="cyan", nl=False)
    click.secho(f"{len(scanning_result.get("directories", 0))}", fg="yellow", bold=True)
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
    click.secho(" ✅ Done!\n", fg="green", bold=True)

@main.command()
@click.argument("path", required=False, default=None)
def git_analyze(path):
    cwd = scan_and_validate(path)

    click.secho("")
    click.secho("─" * 50, fg="bright_black")
    click.secho(f"📂 Scanning: ", fg="cyan", bold=True, nl=False)
    click.secho(f"{cwd}", fg="white")

    git_info = analyze_git_repository(path)

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

@main.command()
@click.argument("path", required=False, default=None)
def languages(path):
    cwd = scan_and_validate(path)

    click.secho("")
    click.secho("─" * 50, fg="bright_black")
    click.secho(f"📂 Scanning: ", fg="cyan", bold=True, nl=False)
    click.secho(f"{cwd}", fg="white")

    scanning_result = repo_scan_findings(cwd)
    files = scanning_result.get("files", [])

    languages = languages_present(files=files)
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

"""
    analyze_result = analyze_repo(scanning_result["files"], scanning_result['has_test'], directories=scanning_result['directories'])
    print("==========================")
    print("Deep Analysis")
    print("==========================")
    print("File LOC Breakdown")
    print("===========================")
    for file , loc in analyze_result['file_lines'].items():
        print(f"{file} : {loc} LOC")
    
    print("=================================")
    print("Dependencies used")
    print("=================================")
    for file , dep in analyze_result['dep'].items():
        print("File:               " , file)
        print("Ecosystem:          " , dep['ecosystem'])
        print("Package Manager:    " , dep['package_manager'])
        print("Dependencies:       " , dep['dependencies'])
        print("Total dependencies: " , dep['dep_count'])            
        print("Frameworks:         " , dep['framework'] if dep['framework'] else {}),
        print("Total Frameworks:   " , len(dep['framework']))
        print("Category:           " , dep['framework_categories'] if dep['framework_categories'] else {})
        print("==============================")
"""

if __name__ == "__main__":
    main()