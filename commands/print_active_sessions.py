from cat.looking_glass.stray_cat import StrayCat

from pympler import asizeof

def print_active_sessions(cat: StrayCat):

    active_sessions = {}

    active_sessions["sessions_count"] = len(cat._StrayCat__ws.app.state.strays)
    active_sessions["sessions"] = []

    for session_id, stray_cat in cat._StrayCat__ws.app.state.strays.items():
        session = {}

        session["session_id"] = session_id
        session["user"] = stray_cat.user_id
        session["history_length"] = len(stray_cat.working_memory.history)
        session["working_memory_size"] = asizeof.asizeof(stray_cat.working_memory)
        session["event_loop_id"] = "main event loop" #id(stray_cat.loop)

        active_sessions["sessions"].append(session)

    output = f"""

**`Active sessions`**

||||
|-|-|-|
|User ID|User Name|History Length|Working Memory Size (KB)|Event Loop ID
"""
    for session in active_sessions["sessions"]:
        output += f"""|{session["session_id"]}|{session["user"]}|{session["history_length"]}|{session["working_memory_size"]}|{session["event_loop_id"]}
"""

    return {"output": output}
