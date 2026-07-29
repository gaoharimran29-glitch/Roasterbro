import click

def print_dep_output(dep: dict):
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
