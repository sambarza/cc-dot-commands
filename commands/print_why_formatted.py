from cat.looking_glass.stray_cat import StrayCat


def print_why_formatted(cat: StrayCat):

    if len(cat.working_memory.history) < 2:
        return {"output": "No answer yet"}

    last_why = cat.working_memory.history[-2]["why"]

    cat.send_chat_message(
        f"""
```text
Last question was:
```
{last_why.input}
""",
        save=False,
    )

    if len(last_why.intermediate_steps) == 0:
        cat.send_chat_message(f"""No tool used""", save=False)

    for intermediate_step in last_why.intermediate_steps:

        cat.send_chat_message(
            f"""
| | |
|-|-|
|**Tool used:**| `{intermediate_step[0][0]}`|
|**Input:**| `{intermediate_step[0][1]}`|
|**Output:**| `{intermediate_step[1]}`|
""",
            save=False,
        )

    for model_interaction in last_why.model_interactions:

        if model_interaction.model_type != "llm":
            continue

        prompt = model_interaction.prompt.replace('"', "'")
        reply = model_interaction.reply.replace('"', "'")

        cat.send_chat_message(
            f"""
| | |
|-|-|
|**Agent Source:**| `{model_interaction.source}`|
|**Duration in secs:**|`{model_interaction.ended_at - model_interaction.started_at}`|
|**Input tokens:**|`{model_interaction.input_tokens}`|
|**Output tokens:**|`{model_interaction.output_tokens}`|
```text
```
**Prompt**
{prompt}
```text
```
**Reply**
```text
{reply}
```
""",
            save=False,
        )

    return {
        "output": f"""
```text
Answer was:
```
{cat.working_memory.history[-2]["message"]}
"""
    }
