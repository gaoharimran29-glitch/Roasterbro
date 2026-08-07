import json
import click
from git import Head
from langchain_core.prompts import ChatPromptTemplate

from roasterbro.tools.repo_basic_scan import repo_scan_findings
from roasterbro.tools.repo_deps_scan import dependencies_analyzer
from roasterbro.tools.repo_file_scan import file_metrics
from roasterbro.tools.repo_git_scan import analyze_git_repository
from roasterbro.tools.repo_lang_scan import languages_present

from roasterbro.prompts.final_roast_prompt import FINAL_ROAST_SYSTEM_PROMPT, FINAL_ROAST_USER_PROMPT
from roasterbro.prompts.facts_extract_prompt import EXTRACT_SYSTEM_PROMPT, EXTRACT_USER_PROMPT
from roasterbro.prompts.questions_generate_prompt import QUESTION_SYSTEM_PROMPT, QUESTION_USER_PROMPT

from roasterbro.models.roast_output_model import RagebaitResponse, FinalRoast, RepoFacts
from langsmith import traceable

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


@traceable(name="Roasterbro")
async def generate_roast(scan_data: dict, llm):
    scan_data = make_json_safe(scan_data)

    structured_llm_facts = llm.with_structured_output(RepoFacts)
    structured_llm_questions = llm.with_structured_output(RagebaitResponse)
    structured_llm_roast = llm.with_structured_output(FinalRoast)

    click.secho("🥱 Digging through your repo for ammo...", fg="yellow")
    click.secho("")
    prompt_facts = ChatPromptTemplate.from_messages([("system", EXTRACT_SYSTEM_PROMPT), ("human", EXTRACT_USER_PROMPT)])
    prompt_facts_value = await prompt_facts.ainvoke({"scan_data": json.dumps(scan_data, ensure_ascii=False, indent=2)})
    messages_facts = prompt_facts_value.to_messages()

    try:
        generated_facts: RepoFacts = await structured_llm_facts.ainvoke(messages_facts)
    except Exception as e:
        click.secho(f"\n❌ Analysis Failed.", fg="red", bold=True)
        click.secho(f"\n❌ Validation Error: Local model failed to match JSON schema. {e}", fg="red", bold=True)
        raise click.exceptions.Exit(1)

    click.secho("😈 Cooking up some questions for you, bro...", fg="yellow")

    prompt_questions = ChatPromptTemplate.from_messages([("system", QUESTION_SYSTEM_PROMPT), ("human", QUESTION_USER_PROMPT)])
    prompt_questions_value = await prompt_questions.ainvoke({"facts": generated_facts.facts})
    messages_questions = prompt_questions_value.to_messages()

    try:
        generate_questions: RagebaitResponse = await structured_llm_questions.ainvoke(messages_questions)
    except Exception as e:
        click.secho("Taunts Generation Failed", fg="red", bold=True)
        click.secho(f"\n❌ Validation Error: Local model failed to match JSON schema. {e}", fg="red", bold=True)
        raise click.exceptions.Exit(1)

    interrogation_history = []

    for idx, q_item in enumerate(generate_questions.questions, start=1):
        click.echo()
        click.secho(f"❓ Question {idx}/{len(generate_questions.questions)}: {q_item.question}", fg="bright_cyan", bold=True)
        
        tags = [chr(65 + i) for i in range(len(q_item.options))]
        for tag, option in zip(tags, q_item.options):
            click.secho(f"({tag}) {option}", fg="bright_cyan")
        click.echo()

        while True:
            try:
                user_input = click.prompt(click.style("Your Answer (A/B/C)", fg="green", bold=True)).strip().upper()
            except click.exceptions.Abort:
                click.echo()
                click.secho("✖ Roast aborted. Coward.", fg="red")
                raise click.exceptions.Exit(1)
            
            if user_input in tags:
                selected_option_text = q_item.options[tags.index(user_input)]
                break
            
            click.echo()
            click.secho("ERROR: Choose only from given options (A, B, or C)", fg="red", bold=True)
            click.echo()

        interrogation_history.append(f"Question: {q_item.question}")
        interrogation_history.append(f"User selected Option {user_input}: {selected_option_text}")

    conversation_text = "\n".join(interrogation_history)

    prompt_roast = ChatPromptTemplate.from_messages([("system", FINAL_ROAST_SYSTEM_PROMPT), ("human", FINAL_ROAST_USER_PROMPT)])
    prompt_roast_value = await prompt_roast.ainvoke({"facts": generated_facts.facts, "qa_pairs":conversation_text})
    messages_roast = prompt_roast_value.to_messages()

    click.secho("")
    click.secho("💀 Drafting my closing statement on this crime scene...", fg="yellow")
    click.echo()
    click.secho("─" * 50, fg="bright_black")
    click.secho("🔥 REPO ROAST — don't take it personal, bro 🔥", fg="red", bold=True)
    click.secho("─" * 50, fg="bright_black")
    click.echo()

    try:
        final_roast_obj: FinalRoast = await structured_llm_roast.ainvoke(messages_roast)
        click.secho(final_roast_obj.roast, fg="bright_cyan")
        click.secho("")
        click.secho(f"💀 {final_roast_obj.mic_drop_line}", fg="red", bold=True)

    except Exception as e:
        click.secho(f"\n❌ Final roast not generated: {e}", fg="red")
        raise click.exceptions.Exit(1)

    click.echo()
    click.secho("─" * 70, fg="red")
