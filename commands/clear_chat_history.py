from cat.looking_glass.stray_cat import StrayCat


def clear_chat_history(command, cat: StrayCat):

    # Command without parameters?
    if command == ".ch":

        # Clear all memories
        cat.working_memory.episodic_memories.clear()
        cat.working_memory.history.clear()

        return {"output": "Ok I have forgotten everything"}

    else:

        # Clear all memories after nnn
        remove_after = int(command.split(" ")[1])

        cat.working_memory.episodic_memories = cat.working_memory.episodic_memories[
            0:remove_after
        ]
        cat.working_memory.history = cat.working_memory.history[0:remove_after]

        return {"output": f"Ok I have forgotten everything after {remove_after}"}
