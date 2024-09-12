from cat.looking_glass.stray_cat import StrayCat


def remove_last_turn(cat: StrayCat):
    cat.working_memory.history = cat.working_memory.history[0:-3]
    return {"output": "Ok I have removed the last turn"}
