from time import sleep

from cat.looking_glass.stray_cat import StrayCat

def sleep_thread(cat: StrayCat):

    sleep_time = int(cat.working_memory.user_message_json.text.split(" ")[1])

    sleep(sleep_time)

    return {"output": f"Slept for {sleep_time} seconds"}