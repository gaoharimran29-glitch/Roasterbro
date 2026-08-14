import click
import json
import asyncio

from roasterbro.utils.helpers import scan_and_validate
from roasterbro.utils.config import get_llm
from roasterbro.tools.repo_basic_scan import repo_scan_findings
from roasterbro.tools.repo_deps_scan import dependencies_analyzer
from roasterbro.tools.repo_file_scan import file_metrics
from roasterbro.tools.repo_git_scan import analyze_git_repository
from roasterbro.tools.repo_lang_scan import languages_present
from roasterbro.tools.repo_whitespace_scan import whitespace_scan
from roasterbro.tools.repo_roast_scan import full_scan_for_roast, generate_roast, make_json_safe
from roasterbro.tools.find_llm_models import find_models

from roasterbro.output_formatter.scan_output_formatter import print_scan_output
from roasterbro.output_formatter.git_output_formatter import print_git_output
from roasterbro.output_formatter.lang_output_formatter import print_lang_output
from roasterbro.output_formatter.dep_output_formatter import print_dep_output
from roasterbro.output_formatter.filestats_output_formatter import print_filestats_output
from roasterbro.output_formatter.whitespace_output_formatter import print_whitespace_output
from roasterbro.output_formatter.model_output_formatter import print_model_output


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
│           A CLI that scans your codebase, interrogates you and then roasts it. - 0.1.0                 │
│                                   Made by - Gaohar Imran                                                │
│                                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────╯
"""

class AliasedGroup(click.Group):

    aliases = {
        "-s": "scan",
        "-g": "gitanalyze",
        "-d": "deps",
        "-l": "langs",
        "-fs": "filestats",
        "-w": "whitespace",
        "-f": "fullscan",
        "-m": "models",
        "-r": "roast"
    }


    def get_command(self, ctx, cmd_name):
        actual_name = self.aliases.get(cmd_name, cmd_name)
        return click.Group.get_command(self, ctx, actual_name)


    def list_commands(self, ctx):
        return click.Group.list_commands(self, ctx)


    def format_commands(self, ctx, formatter):
        rows = []
        
        reverse_aliases = {v: k for k, v in self.aliases.items()}

        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            if cmd is None:
                continue
            
            shortcut = reverse_aliases.get(subcommand)
            if shortcut:
                display_name = f"{shortcut}, {subcommand}"
            else:
                display_name = subcommand
                
            help_text = cmd.get_short_help_str() or ""
            rows.append((display_name, help_text))

        if rows:
            with formatter.section("Commands"):
                formatter.write_dl(rows)


@click.group(context_settings={"help_option_names": ["-h", "--help"], "ignore_unknown_options":True}, invoke_without_command=True, cls=AliasedGroup)
@click.version_option("0.1.0", "-v", "--version", prog_name="Roasterbro", message="%(prog)s %(version)s")
@click.pass_context
def main(ctx) -> None:
    """RoasterBro - A CLI to roast and scan your codebase."""
    if ctx.invoked_subcommand is None:
        click.secho(BANNER, fg="green", bold=True)
        click.secho(
        "For more information, please visit the project repository at "
        "https://github.com/gaoharimran29-glitch/Roasterbro or reach out to the "
        "developer directly. If you encounter any bugs or security "
        "vulnerabilities, kindly report them to the developer. For assistance, "
        "run 'roasterbro --help' or 'roasterbro -h'.",
        fg="magenta", bold=True, underline=True
    )


@main.command()
@click.argument("path", required=False, default=None)
def scan(path: str | None) -> None:
    """Return basic info about the repo"""
    cwd = scan_and_validate(path, "scan")
    scanning_result = repo_scan_findings(cwd)
    print_scan_output(scanning_result)
    click.secho(" ✨ Done!\n", fg="green", bold=True)


@main.command()
@click.argument("path", required=False, default=None)
def gitanalyze(path: str | None) -> None:
    """Return git info about the repo"""
    cwd = scan_and_validate(path, "gitanalyze")
    git_info = analyze_git_repository(cwd)
    print_git_output(git_info)
    click.secho(" ✨ Done!\n", fg="green", bold=True)


@main.command()
@click.argument("path", required=False, default=None)
def langs(path: str | None) -> None:
    """Return all the languages used in the repo"""
    cwd = scan_and_validate(path, "langs")
    scanning_result = repo_scan_findings(cwd)
    files = scanning_result.get("files", [])
    languages = languages_present(files=files)
    print_lang_output(languages)
    click.secho(" ✨ Done!\n", fg="green", bold=True)


@main.command()
@click.argument("path", required=False, default=None)
def deps(path: str | None) -> None:
    """Return all the dependencies used in the repo"""
    cwd = scan_and_validate(path, "deps")
    scanning_result = repo_scan_findings(cwd)
    files = scanning_result.get("files", [])
    dep = dependencies_analyzer(files=files)
    print_dep_output(dep)
    click.secho(" ✨ Done!\n", fg="green", bold=True)


@main.command()
@click.argument("path", required=False, default=None)
def filestats(path: str | None) -> None:
    """Return stats related to files in the repo"""
    cwd = scan_and_validate(path, "filestats")
    scanning_result = repo_scan_findings(cwd)
    files = scanning_result.get("files", [])
    directories = scanning_result.get("directories" , [])
    has_test = scanning_result.get("has_test", False)
    stats = file_metrics(files=files, has_test=has_test, directories=directories)
    print_filestats_output(stats)
    click.secho(" ✨ Done!\n", fg="green", bold=True)


@main.command()
@click.argument("path", required=False, default=None)
def whitespace(path: str | None) -> None:
    """Return filename and line number for trailing whitespace"""
    cwd = scan_and_validate(path, "whitespace")
    scanning_result = repo_scan_findings(cwd)
    files = scanning_result.get("files", [])
    whitespaces = whitespace_scan(files)
    print_whitespace_output(whitespaces)
    click.secho(" ✨ Done!\n", fg="green", bold=True)


@main.command()
@click.argument("path", required=False, default=None)
@click.option(
    "--json", "json_path",
    type=click.Path(writable=True, file_okay=True, dir_okay=False),
    default=None,
    help="To save the output in the json file"
)
def fullscan(path: str | None, json_path: str | None) -> None:
    """Run a combined full scan (with optional JSON export"""
    cwd = scan_and_validate(path, "fullscan")
    scanning_result = repo_scan_findings(cwd)
    print_scan_output(scanning_result)

    files = scanning_result.get("files", [])
    languages = languages_present(files=files)
    print_lang_output(languages)

    dep = dependencies_analyzer(files=files)
    print_dep_output(dep)

    directories = scanning_result.get("directories" , [])
    has_test = scanning_result.get("has_test", False)
    stats = file_metrics(files=files, has_test=has_test, directories=directories)
    print_filestats_output(stats)

    git_info = analyze_git_repository(cwd)
    print_git_output(git_info)

    if json_path:

        combined_data = {
            "scanning_result": scanning_result,
            "languages": languages,
            "dependencies": dep,
            "file_stats": stats,
            "git_info": git_info
        }

        combined_data = make_json_safe(combined_data)

        try:

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(combined_data, f, indent=4, ensure_ascii=False)

            click.echo(click.style(f"\n💾 Successfully saved scan results to: {json_path}", fg="green"))

        except Exception as e:
            click.echo(click.style(f"\n❌ Failed to save JSON file: {e}", fg="red"), err=True)

    click.secho(" ✨ Done!\n", fg="green", bold=True)


@main.command()
def models() -> None:
    """Detect local LLM models and cloud LLM provider API keys"""
    result = find_models()
    print_model_output(result)
    click.secho(" ✨ Done!\n", fg="green", bold=True)


@main.command()
@click.argument("path", required=False, default=None)
@click.option(
    "--provider", 
    type=str, 
    default="google",
    help="Specify the LLM Model provider company (e.g., google)"
)
@click.option(
    "--llm", 
    type=str, 
    default="gemini-2.5-flash-lite",
    help="Specify the LLM model to use (e.g., gemini-2.5-flash-lite)."
)
def roast(path: str | None, llm: str, provider: str) -> None:
    """Interrogate the developer with 3 repository-based ragebait questions and generate a final AI roast"""
    cwd = scan_and_validate(path, "roast")
    llm_instance = get_llm(provider, llm)
    result = full_scan_for_roast(cwd)
    asyncio.run(generate_roast(result, llm=llm_instance))


if __name__ == "__main__":
    main()
