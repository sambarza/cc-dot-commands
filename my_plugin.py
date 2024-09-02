import time
from cat.mad_hatter.decorators import tool, hook
from cat.looking_glass.cheshire_cat import CheshireCat

original_user_message_json = ""


@hook
def agent_fast_reply(fast_reply, cat: CheshireCat):
    """Use this hook to reply fast to the user"""

    if cat.working_memory["user_message_json"]["text"] == ".p":

        return formatted_chat_history(cat)

    if cat.working_memory["user_message_json"]["text"] == ".cc":

        cat.working_memory.episodic_memories.clear()
        cat.working_memory["history"].clear()

        return {"output": "Ok I have forgotten everything"}

    if cat.working_memory["user_message_json"]["text"] == ".lp":

        return {"output": cat.working_memory.last_used_prompt}

    if cat.working_memory["user_message_json"]["text"] == ".rl":
        cat.working_memory.remove_last_turn()
        return {"output": "Ok I have removed the last turn"}

    if cat.working_memory["user_message_json"]["text"][:2] == ".k":
        turns_to_keep = int(
            cat.working_memory["user_message_json"]["text"].split(" ")[1]
        )

        if turns_to_keep % 2 != 0:
            return {"output": f"{turns_to_keep} is HUMAN turn, specify an AI turn"}

        cat.working_memory.keep_up_to_turn(turns_to_keep)

        return formatted_chat_history(cat)

    if "original_text" in cat.working_memory["user_message_json"].keys():

        original_user_message_text = cat.working_memory["user_message_json"][
            "original_text"
        ]

        if original_user_message_text[:2] == ".r":

            # Remove the original message
            del cat.working_memory["user_message_json"]["original_text"]

            return None

    if cat.working_memory["user_message_json"]["text"] == ".":

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
      """

        return {"output": commands}


def formatted_chat_history(cat):

    if len(cat.working_memory["history"]) == 0:
        return {"output": "Chat history is empty"}

    history = ""

    turn_number = 0
    for turn in cat.working_memory["history"]:
        turn_number += 1

        history += (
            f"\n *{str(turn_number).zfill(3)}* - {turn['who']}: {turn['message']}"
        )

    return {"output": history}


@hook
def before_cat_reads_message(user_message_json, cat: CheshireCat):

    # Remove dot commands in history
    if cat.working_memory["history"][-2]["message"][0] == ".":
        cat.working_memory["history"] = cat.working_memory["history"][:-2]

    # Exit if not resend command
    if not user_message_json["text"][:2] == ".r":
        return

    # Keep the original message, will be used in hook agent_fast_reply
    user_message_json["original_text"] = user_message_json["text"]

    # Answer to resend has been specified?
    if len(user_message_json["text"].split(" ")) > 1:
        # Answer to resend has been specified
        turn_to_resend = int(user_message_json["text"].split(" ")[1])
    else:
        # Answer to resend has not been specified, resend the last answer
        turn_to_resend = int(len(cat.working_memory["history"]) - 1)

    # Keep the history up to the answer to resend
    turns_to_keep = turn_to_resend - 1

    # Get the question
    question = cat.working_memory["history"][turn_to_resend - 1]["message"]

    # Keep the history up to the answer to resend
    cat.working_memory.keep_up_to_turn(turns_to_keep)

    # Replace the question
    user_message_json["text"] = question

    return user_message_json
