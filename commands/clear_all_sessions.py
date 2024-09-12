from cat.looking_glass.stray_cat import StrayCat


def clear_all_sessions(cat: StrayCat):

    for stray in cat._StrayCat__ws.app.state.strays.values():
        stray._StrayCat__ws.close()

    cat._StrayCat__ws.app.state.strays.clear()

    return {"output": "All sessions removed"}
