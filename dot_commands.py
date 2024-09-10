from cat.mad_hatter.decorators import hook
from cat.looking_glass.stray_cat import StrayCat
from cat.convo.messages import Role
from cat.convo.messages import CatMessage

import json


@hook
def agent_fast_reply(fast_reply, cat: StrayCat):
    """Use this hook to reply fast to the user"""

    # Not a dot command
    if cat.working_memory.user_message_json.text[0] != ".":
        return

    if cat.working_memory.user_message_json.text == ".ph":

        return formatted_chat_history(cat)

    if cat.working_memory.user_message_json.text == ".ch":

        cat.working_memory.episodic_memories.clear()
        cat.working_memory.history.clear()

        return {"output": "Ok I have forgotten everything"}

    if cat.working_memory.user_message_json.text == ".rt":
        cat.working_memory.history = memory_remove_last_turn(cat.working_memory.history)
        return {"output": "Ok I have removed the last turn"}

    if cat.working_memory.user_message_json.text[:2] == ".kh":
        turns_to_keep = int(cat.working_memory.user_message_json.text.split(" ")[1])

        if turns_to_keep % 2 != 0:
            return {"output": f"{turns_to_keep} is HUMAN turn, specify an AI turn"}

        cat.working_memory.history = memory_keep_up_to_turn(
            cat.working_memory.history, turns_to_keep
        )

        return formatted_chat_history(cat)

    if cat.working_memory.user_message_json.text == ".as":
        active_sessions = {}

        active_sessions["sessions_count"] = len(cat._StrayCat__ws.app.state.strays)
        active_sessions["sessions"] = []

        for session_id, stray_cat in cat._StrayCat__ws.app.state.strays.items():
            session = {}

            session["session_id"] = session_id
            session["user"] = stray_cat.user_id
            session["history_length"] = len(stray_cat.working_memory.history)

            active_sessions["sessions"].append(session)

        output = f"""
||||
|-|-|-|
|ID|User|History Length |
"""
        for session in active_sessions["sessions"]:
            output += f"""|{session["session_id"]}|{session["user"]}|{session["history_length"]}|
"""

        return {"output": output}

    if cat.working_memory.user_message_json.text == ".whoami":
        return {"output": str(cat.user_id)}

    if cat.working_memory.user_message_json.text == ".cs":

        for stray in cat._StrayCat__ws.app.state.strays.values():
            stray._StrayCat__ws.close()

        cat._StrayCat__ws.app.state.strays.clear()

        return {"output": "All sessions removed"}

    if cat.working_memory.user_message_json.text == ".lw":

        if len(cat.working_memory.history) < 2:
            return {"output": "No answer yet"}

        last_why = cat.working_memory.history[-2]["why"]

        if len(last_why.intermediate_steps) == 0:
            cat.send_chat_message(f"""No tool used""", save=False)

        for intermediate_step in last_why.intermediate_steps:

            cat.send_chat_message(
                f"""
| | |
|-|-|
|**Tool:**| `{intermediate_step[0][0]}`|
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
|**Source:**| `{model_interaction.source}`|
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
Question was:
```text
{last_why.input}
```
"""
        }

    if cat.working_memory.user_message_json.text == ".lwr":

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

    if cat.working_memory.user_message_json.text == ".lp":

        active_plugins_count = 0
        inactive_plugins_count = 0

        for plugin in cat.mad_hatter.plugins.values():

            if plugin.id == "core_plugin":
                continue

            if plugin.active:
                active_plugins_count += 1
            else:
                inactive_plugins_count += 1

            output = f"""
**`{plugin.id}:  {"active" if plugin.active else "not active"}`**
"""
            if len(plugin.tools) > 0:
                output += """
```
```
**Implemented Tools**
| | |
|-|-|
|`Name` | `Description`| `Return Direct`
"""
                for tool in plugin.tools:
                    output += f"""|`{tool.name}`|`{tool.description}`|{tool.return_direct}\n"""

            if len(plugin.hooks) > 0:
                output += """
```
```
**Used hooks**
|||
|-|-|
|`Name`|`Priority`|
"""

                for hook in plugin.hooks:
                    output += f"""|`{hook.name}`|`{hook.priority}`|\n"""

            cat.send_chat_message(output, save=False)

        return {
            "output": f"{active_plugins_count} active plugins / {inactive_plugins_count} inactive plugins"
        }

    if cat.working_memory.user_message_json.text == ".":

        commands = """
**`Dot Commands`**
```
```
*`History manipulation`*
```text
[.ph]     - Print chat History
[.ch]     - Clear chat History
[.rt]     - Remove last Turn
[.kh nnn] - Keep chat History up to nnn turns
[.sh]     - Save chat History (not implemented)
[.lh]     - Load chat History (not implemented)
```

*`Quick resend`*
```text
[.r]      - Resend the last question
[.r nnn]  - Resend a specific HUMAN question
```

*```"Why" of last answer```*
```text
[.lw]     - Print last "why" formatted
[.lwr]    - Print last "why" in raw format
```
*`Plugins management`*
```text
[.lp]     - List installed plugins
```

*`Sessions management`*
```text
[.whoami] - Print current user
[.as]     - Print active sessions
[.cs]     - Clear all sessions (cannot close ws sessions??)
```
"""

        return {"output": commands}


def formatted_chat_history(cat: StrayCat):

    # 2 because memory history already contains the dot command
    if len(cat.working_memory.history) < 2:
        return {"output": "Chat history is empty"}

    history = ""

    turn_number = 0
    for turn in cat.working_memory.history[0:-1]:
        turn_number += 1

        history += f"\n {str(turn_number).zfill(3)} {turn['who']}: {turn['message']}"

    return {
        "output": f"""
```text
{history}
```
"""
    }


@hook
def before_cat_reads_message(user_message_json, cat: StrayCat):

    cleaned_history = []

    # Remove all the dot commands questions and answer
    for turn in cat.working_memory.history:

        if turn["role"] == Role.AI:
            if turn["why"].input[0] == ".":
                continue

        if turn["role"] == Role.Human:
            if turn["message"][0] == ".":
                continue

        cleaned_history.append(turn)

    cat.working_memory.history = cleaned_history

    # Exit if the prompt is not a resend command
    if not user_message_json.text[:2] == ".r":
        return

    # Question to resend has been specified?
    if len(user_message_json.text.split(" ")) > 1:
        # Question to resend has been specified
        question_to_resend = int(user_message_json.text.split(" ")[1])
    else:
        # Question to resend has not been specified, resend the last answer
        question_to_resend = int(len(cat.working_memory.history) - 1)

    # The question index is 0 based however the user ask for question 1 based
    index_of_question_to_resend = question_to_resend - 1

    # Get the question text
    question = cat.working_memory.history[index_of_question_to_resend]["message"]

    # Keep the history up to the answer to resend
    turns_to_keep = index_of_question_to_resend

    # Keep the history up to the question to resend
    cat.working_memory.history = memory_keep_up_to_turn(
        cat.working_memory.history, turns_to_keep
    )

    # Replace the question
    user_message_json.text = question

    return user_message_json


def memory_remove_last_turn(history):
    return history[0:-2]


def memory_keep_up_to_turn(history, turns_to_keep):
    return history[0:turns_to_keep]
