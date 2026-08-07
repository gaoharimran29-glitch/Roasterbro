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
from git import Head
from roasterbro.models.roast_output_model import RagebaitResponse, FinalRoast

def make_json_safe(obj):
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, (set, tuple)):
        return list(obj)
    elif isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    elif isinstance(obj, Head):
        return str(obj)
    else:
        return obj


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


async def generate_roast(scan_data: dict, llm):
    scan_data = make_json_safe(scan_data)
    
    structured_llm_questions = llm.with_structured_output(RagebaitResponse)
    structured_llm_roast = llm.with_structured_output(FinalRoast)

    prompt = ChatPromptTemplate.from_messages([("system", SYSTEM_PROMPT), ("human", USER_PROMPT)])
    prompt_value = await prompt.ainvoke({"scan_data": json.dumps(scan_data, ensure_ascii=False, indent=2)})
    messages = prompt_value.to_messages()

    click.secho("🤖 Generating interrogation questions...", fg="yellow")
    try:
        structured_response: RagebaitResponse = await structured_llm_questions.ainvoke(messages)
    except Exception as e:
        click.secho(f"\n❌ Validation Error: Local model failed to match JSON schema. {e}", fg="red", bold=True)
        raise click.Abort()

    interrogation_history = []

    for idx, q_item in enumerate(structured_response.questions, start=1):
        click.echo()
        click.secho(f"❓ Question {idx}: {q_item.question}", fg="bright_cyan", bold=True)
        
        tags = ["A", "B", "C"]
        for tag, option in zip(tags, q_item.options):
            click.secho(f"{option}", fg="bright_cyan")
        click.echo()

        while True:
            user_input = click.prompt(click.style("Your Answer (A/B/C)", fg="green", bold=True)).strip().upper()
            if user_input in tags:
                selected_option_text = q_item.options[tags.index(user_input)]
                break
            
            click.echo()
            click.secho("ERROR: Choose only from given options (A, B, or C)", fg="red", bold=True)
            click.echo()

        interrogation_history.append(f"Question: {q_item.question}")
        interrogation_history.append(f"User selected Option {user_input}: {selected_option_text}")

    conversation_text = "\n".join(interrogation_history)
    
    final_messages = [
        SystemMessage(content=FINAL_ROAST_PROMPT),
        HumanMessage(content=f"Here is the data from the interrogation session:\n\n{conversation_text}\n\nNow give the final roast based on this.")
    ]

    click.echo()
    click.secho("─" * 50, fg="bright_black")
    click.secho("🔥 REPO ROAST", fg="red", bold=True)
    click.secho("─" * 50, fg="bright_black")
    click.echo()

    try:
        final_roast_obj: FinalRoast = await structured_llm_roast.ainvoke(final_messages)
        click.secho(final_roast_obj.roast, fg="bright_cyan")

    except Exception as e:
        click.secho(f"\n❌ Error generating final structured roast: {e}", fg="red")
        raise click.Abort()

    click.echo()
    click.secho("─" * 70, fg="red")
