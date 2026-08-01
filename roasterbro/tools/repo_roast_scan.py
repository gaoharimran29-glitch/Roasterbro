from roasterbro.tools.repo_basic_scan import repo_scan_findings
from roasterbro.tools.repo_deps_scan import dependencies_analyzer
from roasterbro.tools.repo_file_scan import file_metrics
from roasterbro.tools.repo_git_scan import analyze_git_repository
from roasterbro.tools.repo_lang_scan import languages_present
from roasterbro.prompts.roaster_prompt import SYSTEM_PROMPT, USER_PROMPT, FINAL_ROAST_PROMPT
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import click
from ollama._types import ResponseError


def make_json_safe(obj):
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, (set, tuple)):
        return list(obj)
    elif isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    else:
        return obj


def stream_and_print(messages, llm, color="white",):
    full_text = ""
    try:
        for chunk in llm.stream(messages):
            piece = chunk.content
            if piece:
                click.secho(piece, fg=color, nl=False)
                full_text += piece
        click.echo()
        return full_text

    except ResponseError as e:
        if e.status_code == 404:
            click.echo(
                f"\n❌ Error: The model you requested was not found in Ollama.\n"
                f"Please make sure it's downloaded using: 'ollama pull <model_name>'", 
                err=True
            )
        else:
            click.echo(f"\n❌ Ollama Error: {e.error}", err=True)
        raise click.Abort()


def full_scan_for_roast(cwd):

    scanning_result = repo_scan_findings(cwd)

    files = scanning_result.get("files", [])
    languages = languages_present(files=files)

    dep = dependencies_analyzer(files=files)

    directories = scanning_result.get("directories" , [])
    has_test = scanning_result.get("has_test", False)
    stats = file_metrics(files=files, has_test=has_test, directories=directories)

    git_info = analyze_git_repository(cwd)

    del scanning_result['files']
    del scanning_result['directories']
    del stats['file_sizes']

    return {
        "Repo Info": scanning_result,
        "Languages": languages,
        "Dependencies": dep,
        "File Stats": stats,
        "Git Info": git_info
    }


def generate_roast(scan_data: dict, llm):
    llm_instance = llm
    scan_data = make_json_safe(scan_data)

    prompt = ChatPromptTemplate.from_messages([("system", SYSTEM_PROMPT), ("human", USER_PROMPT)])

    messages = prompt.invoke({"scan_data": json.dumps(scan_data, ensure_ascii=False, indent=2)}).to_messages()
    counter = 1

    while True:

        if counter > 3:
            conversation_text = "\n\n".join(
                f"{'AI' if isinstance(m, AIMessage) else 'User'}: {m.content}"
                for m in messages
                if isinstance(m, (AIMessage, HumanMessage))
            )

            final_message = [
                SystemMessage(content=FINAL_ROAST_PROMPT),
                HumanMessage(content=f"Here is the full conversation do far:\n\n{conversation_text}\n\nNow give the final roast.")
            ]

            click.echo()
            click.secho("─" * 50, fg="bright_black")
            click.secho("🔥 REPO ROAST", fg="red", bold=True)
            click.secho("─" * 50, fg="bright_black")
            click.echo()

            stream_and_print(final_message, color="bright_cyan", llm=llm_instance)
            click.echo()
            click.secho("─" * 70, fg="red")
            break

        result = stream_and_print(messages, color="bright_cyan", llm=llm_instance)

        messages.append(AIMessage(content=result))

        click.secho("")

        while True:
            user_input = click.prompt(click.style("Your Answer", fg="green", bold=True))

            if user_input.lower() in ["a", "b", "c"]:
                break

            click.secho("")
            click.secho("ERROR: Choose only from given option", fg="red", bold=True)
            click.secho("")

        messages.append(HumanMessage(content=user_input))

        counter += 1