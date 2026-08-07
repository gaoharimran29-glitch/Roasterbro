import click

def print_model_output(data: dict):
    ollama_models = data.get("ollama_models", {})
    cloud_providers = data.get("cloud_providers", {})

    # ---- Local Ollama Models ----
    click.secho("\n 🖥️  Local Ollama Models", fg="magenta", bold=True, underline=True)

    if not ollama_models:
        click.secho("  ✖ No local models found", fg="red")
    else:
        max_len = max(len(name) for name in ollama_models)
        total_size = sum(ollama_models.values())

        for name, size in sorted(ollama_models.items(), key=lambda x: x[1], reverse=True):
            color = "green" if size < 5 else "yellow" if size < 15 else "red"
            click.secho(f"  • {name.ljust(max_len)} : ", fg="cyan", nl=False)
            click.secho(f"{size:.2f} GB", fg=color, bold=True)

        click.secho("─" * 50, fg="bright_black")
        click.secho(f"  Total: ", fg="cyan", nl=False)
        click.secho(f"{len(ollama_models)} model(s), {total_size:.2f} GB", fg="green", bold=True)

    # ---- Cloud Providers ----
    click.secho("\n ☁️  Cloud Provider API Keys", fg="magenta", bold=True, underline=True)

    max_len = max(len(name) for name in cloud_providers)
    configured = sum(1 for v in cloud_providers.values() if v)

    for provider, is_set in cloud_providers.items():
        symbol = "✔" if is_set else "✖"
        color = "green" if is_set else "red"
        status = "Configured" if is_set else "Not set"
        click.secho(f"  {symbol} {provider.ljust(max_len)} : ", fg=color, nl=False)
        click.secho(f"{status}", fg=color, dim=not is_set)

    click.secho("─" * 50, fg="bright_black")
    click.secho(f"  Providers configured: ", fg="cyan", nl=False)
    click.secho(f"{configured}/{len(cloud_providers)}", fg="green" if configured else "red", bold=True)
    click.secho("─" * 50, fg="bright_black")
