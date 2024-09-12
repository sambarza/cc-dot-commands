from cat.looking_glass.stray_cat import StrayCat


def print_active_sessions(cat: StrayCat):

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
