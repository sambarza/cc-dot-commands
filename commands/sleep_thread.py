from time import sleep

from cat.looking_glass.stray_cat import StrayCat

def sleep_current_thread(cat: StrayCat):

    sleep_time = int(cat.working_memory.user_message_json.text.split(" ")[1])

    cat.send_chat_message(f"The current thread will sleep for {sleep_time} seconds... *(using time.sleep() inside an hook)*", save=False)

    sleep(sleep_time)

    return {"output": f"The thread slept for {sleep_time} seconds"}