from cat.mad_hatter.decorators import hook
from cat.convo.messages import Role


@hook
def agent_fast_reply(fast_reply, cat):
    """Use this hook to reply fast to the user"""

    # Not a dot command
    if cat.working_memory.user_message_json.text[0] != ".":
        return

    if cat.working_memory.user_message_json.text == ".p":

        return formatted_chat_history(cat)

    if cat.working_memory.user_message_json.text == ".cc":

        cat.working_memory.episodic_memories.clear()
        cat.working_memory.history.clear()

        return {"output": "Ok I have forgotten everything"}

    if cat.working_memory.user_message_json.text == ".lp":

        return {"output": cat.working_memory.last_used_prompt}

    if cat.working_memory.user_message_json.text == ".rl":
        cat.working_memory.history = memory_remove_last_turn(cat.working_memory.history)
        return {"output": "Ok I have removed the last turn"}

    if cat.working_memory.user_message_json.text[:2] == ".k":
        turns_to_keep = int(cat.working_memory.user_message_json.text.split(" ")[1])

        if turns_to_keep % 2 != 0:
            return {"output": f"{turns_to_keep} is HUMAN turn, specify an AI turn"}

        cat.working_memory.history = memory_keep_up_to_turn(
            cat.working_memory.history, turns_to_keep
        )

        return formatted_chat_history(cat)

    if cat.working_memory.user_message_json.text == ".sl":
        active_sessions = {}

        active_sessions["count"] = len(cat._StrayCat__ws.app.state.strays)
        active_sessions["sessions"] = []

        for session_id, stray_cat in cat._StrayCat__ws.app.state.strays.items():
            session = {}

            session["session_id"] = session_id
            session["user"] = stray_cat.user_id
            session["history_length"] = len(stray_cat.working_memory.history)

            active_sessions["sessions"].append(session)

        output = f"Active sessions: {active_sessions['count']}"
        for session in active_sessions["sessions"]:
            output += "\n" + str(session)

        return {"output": output}

    if cat.working_memory.user_message_json.text == ".":

        commands = """
      Dot Commands:
      [.p]     - Print Chat history
      [.k nnn] - Keep Chat History up to nnn turns
      [.r]     - Resend the last question
      [.r nnn] - Resend a specific HUMAN question
      [.cc]    - Clear Chat history
      [.s]     - Save Chat history (not implemented)
      [.l]     - Load Chat history (not implemented)
      [.rl]    - Remove Last turn
      [.lp]    - Print Last Sent Prompt
      [.sl]    - Print active sessions summary
      """

        return {"output": commands}


def formatted_chat_history(cat):

    # 2 because memory history already contains the dot command
    if len(cat.working_memory.history) < 2:
        return {"output": "Chat history is empty"}

    history = ""

    turn_number = 0
    for turn in cat.working_memory.history[0:-1]:
        turn_number += 1

        history += f"\n *{str(turn_number).zfill(3)}* {turn['who']}: {turn['message']}"

    return {"output": history}


@hook
def before_cat_reads_message(user_message_json, cat: CheshireCat):

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
