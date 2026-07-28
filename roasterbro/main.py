from roasterbro.scanner import repo_scan_findings
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
    click.secho(f" 📂 Scanning: ", fg="cyan", bold=True, nl=False)
    click.secho(f"{cwd}", fg="white")

    scanning_result = repo_scan_findings(cwd)

    click.secho(f" 📄 Files Found: ", fg="cyan", nl=False)
    click.secho(f"{len(scanning_result.get("files", 0))}", fg="yellow", bold=True)
    click.secho(f" 📁 Directories Found: ", fg="cyan", nl=False)
    click.secho(f"{len(scanning_result.get("directories", 0))}", fg="yellow", bold=True)
    click.secho("─" * 50, fg="bright_black")

    click.secho("\n Project Important Files Checklist", fg="magenta", bold=True, underline=True)
    click.secho("")
    
    imp_files = scanning_result.get("imp_file", {})
    present_count = sum(1 for v in imp_files.values() if v)
    total_count = len(imp_files)

    max_len = max(len(name) for name in imp_files)

    for name, present in imp_files.items():
        symbol = "✔" if present else "✖"
        color = "green" if present else "red"
        status = "Found" if present else "Missing"
        click.secho(f"  {symbol} {name.ljust(max_len)}  ", fg=color, nl=False)
        click.secho(f"{status}", fg=color, dim=not present)

    click.secho("─" * 50, fg="bright_black")
    score_color = "green" if present_count == total_count else "yellow" if present_count > total_count // 2 else "red"
    click.secho(f" Score: ", fg="cyan", nl=False)
    click.secho(f"{present_count}/{total_count}", fg=score_color, bold=True)
    click.secho("─" * 50, fg="bright_black")
    click.secho(" ✅ Done!\n", fg="green", bold=True)

"""
def main():

    print("Welcome to RoasterBro !")

    parser = argparse.ArgumentParser(description="RoasterBro CLI Scanner")
    parser.add_argument("path",  type=str,  nargs="?",  default=".", 
                        help="The target directory path to scan (defaults to current directory)"
                        )
    args = parser.parse_args()
    
    cwd = Path(args.path).resolve()
    scanning_result = scanner(cwd)
    print("=========================")
    print("Repository Information")
    print("==========================")
    print("Root path: " , scanning_result['root_path'])
    print("Files found: " , len(scanning_result['files']))
    print("Directories Found: " , len(scanning_result['directories']))
    print("==========================")
    print("Files Information")
    print("==========================")
    print("README.md:             " , "Yes" if scanning_result['README.md'] else "No")
    print("LICENSE:               " , "Yes" if scanning_result['LICENSE'] else "No")
    print("Dockerfile:            " , "Yes" if scanning_result['dockerfile'] else "No")
    print("Git Ignore:            " , "Yes" if scanning_result['gitignore'] else "No")
    print("Test Files:            " , "Yes" if scanning_result['has_test'] else "No")
    print("CONTRIBUTING.md:       " , "Yes" if scanning_result['CONTRIBUTING.md'] else "No")
    print("CHANGELOG.md:          " , "Yes" if scanning_result['CHANGELOG.md'] else "No")
    print("CODE_OF_CONDUCT.md:    " , "Yes" if scanning_result['CODE_OF_CONDUCT.md'] else "No")
    print("SECURITY.md:           " , "Yes" if scanning_result['SECURITY.md'] else "No")
    print("CI/CD:                 " , "Yes" if scanning_result['CI/CD'] else "No")
    print("ISSUE_TEMPLATES:       " , "Yes" if scanning_result['ISSUE_TEMPLATES'] else "No")
    print("CODEOWNERS:            " , "Yes" if scanning_result['CODEOWNER'] else "No")
    print("PULL_REQUEST_TEMPLATE: " , "Yes" if scanning_result['PULL_REQUEST_TEMPLATE'] else "No")
    print("FUNDING.yml:           " , "Yes" if scanning_result['FUNDING.yml'] else "No")
    print("Suspicious Files:      " , scanning_result['suspicious_files'])
    print("Total Suspicious Files:" , len(scanning_result['suspicious_files']))
    print("=========================")
    print("Languages Used")
    print("==========================")
    for lang , count in scanning_result['language_present'].items():
        print(f"{lang}: {count}")
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
    print("===================================")
    print("Git Analyze Result")
    print("===================================")
    print("Git Repository:              ", scanning_result.get("Git Repository", False))
    if scanning_result.get("Git Repository"):
        print("Git File Path:           ", scanning_result.get("Hidden Git File Path", None))
        print("Total Contributors:      ", scanning_result.get("Total Contributors", 0))
        print("Total Commits:           ", scanning_result.get("Total Commits", 0))
        print("Last Commit date:        ", scanning_result.get("Last Commit date", None))
        print("Days Since Last Commit:  " , scanning_result.get("Days Since Last Commit", 0))
    else:
        print("Error:                   " , scanning_result.get("Error" , "Unknown Error Occured"))
"""

if __name__ == "__main__":
    main()