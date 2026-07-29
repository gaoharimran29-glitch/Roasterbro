import click
from roasterbro.utils.helpers import scan_and_validate
from roasterbro.tools.repo_basic_scan import repo_scan_findings
from roasterbro.tools.repo_deps_scan import dependencies_analyzer
from roasterbro.tools.repo_file_scan import file_metrics
from roasterbro.tools.repo_git_scan import analyze_git_repository
from roasterbro.tools.repo_lang_scan import languages_present

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
        click.secho("For more information check the repository https://github.com/gaoharimran29-glitch/Roasterbro or contact the developer. " \
        "Please report if any bug or vulnerability found to the developer. For help, use 'roasterbro --help' or 'roasterbro -h' .", fg="magenta", bold=True, underline=True)

@main.command()
@click.argument("path", required=False, default=None)
def scan(path):
    cwd = scan_and_validate(path, "scan")

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
def gitanalyze(path):
    cwd = scan_and_validate(path, "gitanalyze")

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
def lang(path):
    cwd = scan_and_validate(path, "lang")

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

@main.command()
@click.argument("path", required=False, default=None)
def deps(path):
    cwd = scan_and_validate(path, "deps")

    click.secho("")
    click.secho("─" * 50, fg="bright_black")
    click.secho(f"📂 Scanning: ", fg="cyan", bold=True, nl=False)
    click.secho(f"{cwd}", fg="white")

    scanning_result = repo_scan_findings(cwd)
    files = scanning_result.get("files", [])

    dep = dependencies_analyzer(files=files)
    click.secho("\n📦 Dependencies", fg="magenta", bold=True, underline=True)

    if not dep:
        click.secho("  ✖ No dependency files found", fg="red")
        click.secho("─" * 50, fg="bright_black")
        return

    for file_path, info in dep.items():
        click.secho(f"\n  📄 {file_path}", fg="cyan", bold=True)
        click.secho(f"    Ecosystem       : ", fg="yellow", nl=False)
        click.secho(f"{info.get('ecosystem')}", fg="white")
        click.secho(f"    Package Manager : ", fg="yellow", nl=False)
        click.secho(f"{info.get('package_manager')}", fg="white")

        dep_count = info.get("dep_count", 0)
        click.secho(f"    Dependencies    : ", fg="yellow", nl=False)
        click.secho(f"{dep_count}", fg="green" if dep_count else "red", bold=True)

        frameworks = info.get("framework") or set()
        click.secho(f"    Framework(s)    : ", fg="yellow", nl=False)
        if frameworks:
            click.secho(f"{', '.join(sorted(frameworks))}", fg="blue", bold=True)
        else:
            click.secho("None detected", fg="bright_black")

        categories = info.get("framework_categories") or set()
        click.secho(f"    Categories      : ", fg="yellow", nl=False)
        if categories:
            click.secho(f"{', '.join(sorted(categories))}", fg="magenta")
        else:
            click.secho("None detected", fg="bright_black")

        deps_list = info.get("dependencies") or []
        if deps_list:
            click.secho(f"    Packages:", fg="yellow")
            for pkg in deps_list:
                click.secho(f"      • {pkg}", fg="green")

        click.secho("  " + "─" * 46, fg="bright_black")

    click.secho("─" * 50, fg="bright_black")
    click.secho(f"  Total dependency files: ", fg="cyan", nl=False)
    click.secho(f"{len(dep)}", fg="green", bold=True)
    click.secho("─" * 50, fg="bright_black")

@main.command()
@click.argument("path", required=False, default=None)
def filestats(path):
    cwd = scan_and_validate(path, "filemetrics")

    click.secho("")
    click.secho("─" * 50, fg="bright_black")
    click.secho(f"📂 Scanning: ", fg="cyan", bold=True, nl=False)
    click.secho(f"{cwd}", fg="white")

    scanning_result = repo_scan_findings(cwd)
    files = scanning_result.get("files", [])
    directories = scanning_result.get("directories" , [])
    has_test = scanning_result.get("has_test", False)
    
    stats = file_metrics(files=files, has_test=has_test, directories=directories)

    click.secho("\n 📊 Code Statistics", fg="magenta", bold=True, underline=True)

    click.secho(f"  Total LOC          : ", fg="cyan", nl=False)
    click.secho(f"{stats.get('total_loc', 0)}", fg="green", bold=True)

    click.secho(f"  README LOC         : ", fg="cyan", nl=False)
    click.secho(f"{stats.get('readme_loc', 0)}", fg="yellow")

    largest_loc = stats.get("largest_loc_file")
    click.secho(f"  Largest File (LOC) : ", fg="cyan", nl=False)
    click.secho(f"{largest_loc}", fg="blue", bold=True)

    largest_size = stats.get("largest_file_size")
    click.secho(f"  Largest File (Size): ", fg="cyan", nl=False)
    click.secho(f"{largest_size}", fg="blue", bold=True)

    avg_size = stats.get("average_file_size", 0)
    click.secho(f"  Average File Size  : ", fg="cyan", nl=False)
    click.secho(f"{avg_size:.2f} KB" if isinstance(avg_size, (int, float)) else f"{avg_size}", fg="white")

    empty_files = stats.get("empty_files") or []
    click.secho(f"  Empty Files        : ", fg="cyan", nl=False)
    click.secho(f"{len(empty_files)}", fg="red" if empty_files else "green", bold=True)

    files_500 = stats.get("files_gt_500loc") or []
    click.secho(f"  Files > 500 LOC    : ", fg="cyan", nl=False)
    click.secho(f"{len(files_500)}", fg="yellow" if files_500 else "green", bold=True)

    files_1000 = stats.get("files_gt_1000loc") or []
    click.secho(f"  Files > 1000 LOC   : ", fg="cyan", nl=False)
    click.secho(f"{len(files_1000)}", fg="red" if files_1000 else "green", bold=True)

    test_count = stats.get("test_files_count", 0)
    click.secho(f"  Test Files         : ", fg="cyan", nl=False)
    click.secho(f"{test_count}", fg="green" if test_count else "red", bold=True)

    click.secho("─" * 50, fg="bright_black")

    if empty_files:
        click.secho("  ⚠ Empty Files:", fg="red", bold=True)
        for f in empty_files:
            click.secho(f"    - {f}", fg="red")

    if files_1000:
        click.secho("  ⚠ Files exceeding 1000 LOC:", fg="red", bold=True)
        for f in files_1000:
            click.secho(f"    - {f}", fg="red")
    elif files_500:
        click.secho("  ⚠ Files exceeding 500 LOC:", fg="yellow", bold=True)
        for f in files_500:
            click.secho(f"    - {f}", fg="yellow")

    test_files = stats.get("test_files") or []
    if test_files:
        click.secho("  🧪 Test Files:", fg="green", bold=True)
        for f in test_files:
            click.secho(f"    - {f}", fg="green")

    click.secho("─" * 50, fg="bright_black")

if __name__ == "__main__":
    main()