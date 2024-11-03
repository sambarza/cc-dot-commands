from cat.mad_hatter.decorators import hook
from cat.looking_glass.stray_cat import StrayCat

from .commands.print_help import *

from .commands.resend_question import *

from .commands.print_history import *
from .commands.remove_last_turn import *
from .commands.clear_chat_history import *

from .commands.print_why_formatted import *
from .commands.print_why_raw import *

from .commands.list_plugins import *

from .commands.print_current_user import *
from .commands.print_active_sessions import *
from .commands.clear_all_sessions import *

from .commands.threads_info import *
from .commands.sleep_thread import *
from .commands.print_time import *

from .utils import filter_dot_commands

@hook
def agent_fast_reply(fast_reply, cat: StrayCat):

    # Not a dot command
    if cat.working_memory.user_message_json.text[0] != ".":
        return

    # Print help
    if cat.working_memory.user_message_json.text == ".":
        return print_help(cat)

    # Print history
    if cat.working_memory.user_message_json.text == ".ph":
        return print_history(cat)

    # Clear chat history
    if cat.working_memory.user_message_json.text[0:3] == ".ch":
        return clear_chat_history(cat.working_memory.user_message_json.text, cat)

    # Remove last turn
    if cat.working_memory.user_message_json.text == ".rt":
        return remove_last_turn(cat)

    # Print active sessions
    if cat.working_memory.user_message_json.text == ".as":
        return print_active_sessions(cat)

    # Print current user
    if cat.working_memory.user_message_json.text == ".whoami":
        return print_current_user(cat)

    # Clear all sessions
    if cat.working_memory.user_message_json.text == ".cs":
        return clear_all_sessions(cat)

    # Print why formatted
    if cat.working_memory.user_message_json.text == ".lw":
        return print_why_formatted(cat)

    # Print why raw
    if cat.working_memory.user_message_json.text == ".lwr":
        return print_why_raw(cat)

    # List plugins
    if cat.working_memory.user_message_json.text == ".lp":
        return list_plugins(cat)

    # Threads info
    if cat.working_memory.user_message_json.text == ".ti":
        return threads_info(cat)

    # Sleep thread for nnn seconds
    if cat.working_memory.user_message_json.text[:4] == ".st ":
        return sleep_current_thread(cat)

    # Start print time
    if cat.working_memory.user_message_json.text[:4] == ".pt":
        return start_print_time(cat)

    # Unknown dot command
    return {
        "output": f"Unknown dot command `'{cat.working_memory.user_message_json.text}'`"
    }

@hook
def before_cat_reads_message(user_message_json, cat: StrayCat):

    # Remove dot commands from history
    cat.working_memory.history = filter_dot_commands(cat.working_memory.history)

    # Resend question command
    if user_message_json.text == ".r" or user_message_json.text[:3] == ".r ":
        return resend_question(user_message_json, cat)