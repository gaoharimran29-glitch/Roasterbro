import click
from roasterbro.utils.helpers import scan_and_validate
from roasterbro.tools.repo_basic_scan import repo_scan_findings
from roasterbro.tools.repo_deps_scan import dependencies_analyzer
from roasterbro.tools.repo_file_scan import file_metrics
from roasterbro.tools.repo_git_scan import analyze_git_repository
from roasterbro.tools.repo_lang_scan import languages_present

from roasterbro.output_formatter.scan_output_formatter import print_scan_output
from roasterbro.output_formatter.git_output_formatter import print_git_output
from roasterbro.output_formatter.lang_output_formatter import print_lang_output
from roasterbro.output_formatter.dep_output_formatter import print_dep_output
from roasterbro.output_formatter.filestats_output_formatter import print_filestats_output


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
    scanning_result = repo_scan_findings(cwd)
    print_scan_output(scanning_result)


@main.command()
@click.argument("path", required=False, default=None)
def gitanalyze(path):
    cwd = scan_and_validate(path, "gitanalyze")
    git_info = analyze_git_repository(path)
    print_git_output(git_info)


@main.command()
@click.argument("path", required=False, default=None)
def lang(path):
    cwd = scan_and_validate(path, "lang")
    scanning_result = repo_scan_findings(cwd)
    files = scanning_result.get("files", [])
    languages = languages_present(files=files)
    print_lang_output(languages)


@main.command()
@click.argument("path", required=False, default=None)
def deps(path):
    cwd = scan_and_validate(path, "deps")
    scanning_result = repo_scan_findings(cwd)
    files = scanning_result.get("files", [])
    dep = dependencies_analyzer(files=files)
    print_dep_output(dep)


@main.command()
@click.argument("path", required=False, default=None)
def filestats(path):
    cwd = scan_and_validate(path, "filemetrics")
    scanning_result = repo_scan_findings(cwd)
    files = scanning_result.get("files", [])
    directories = scanning_result.get("directories" , [])
    has_test = scanning_result.get("has_test", False)
    stats = file_metrics(files=files, has_test=has_test, directories=directories)
    print_filestats_output(stats)


if __name__ == "__main__":
    main()