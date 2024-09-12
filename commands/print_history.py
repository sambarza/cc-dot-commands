from cat.looking_glass.stray_cat import StrayCat


def print_history(cat: StrayCat):

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
