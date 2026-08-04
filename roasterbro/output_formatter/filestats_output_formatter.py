import click

def print_filestats_output(stats: dict):
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
            if "__init__.py" in f:
                click.secho(f"    - {f}", fg="red", nl=False)
                click.secho(" ( likely intentional - package marker )", fg="red")
            else:
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
