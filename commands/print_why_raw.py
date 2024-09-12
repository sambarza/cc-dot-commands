import json

from cat.looking_glass.stray_cat import StrayCat


def print_why_raw(cat: StrayCat):

    if len(cat.working_memory.history) < 2:
        return {"output": "No answer yet"}

    last_why = cat.working_memory.history[-2]["why"]

    for intermediate_step in last_why.intermediate_steps:

        output = "```\n" + json.dumps(intermediate_step, indent=2)

        cat.send_chat_message(output, save=False)

    for model_interaction in last_why.model_interactions:

        if model_interaction.model_type != "llm":
            continue

        output = "```\n" + json.dumps(model_interaction.model_dump(), indent=2)

        cat.send_chat_message(output, save=False)

    return {
        "output": f"""
Question was:
```text
{last_why.input}
```
"""
    }
