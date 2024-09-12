from cat.looking_glass.stray_cat import StrayCat


# Resend the last human message:
def resend_question(user_message_json, cat: StrayCat):

    # Question to resend has been specified?
    if len(user_message_json.text.split(" ")) > 1:
        # Question to resend has been specified
        question_to_resend = int(user_message_json.text.split(" ")[1])
    else:
        # Question to resend has not been specified, resend the last question
        question_to_resend = int(len(cat.working_memory.history) - 1)

    # The question index is 0 based however the user ask for question 1 based
    index_of_question_to_resend = question_to_resend - 1

    # Get the question text
    question = cat.working_memory.history[index_of_question_to_resend]["message"]

    # Keep the history up to the question to resend
    cat.working_memory.history = cat.working_memory.history[
        0:index_of_question_to_resend
    ]

    # Inform the user of the replaced message
    cat.send_chat_message(
        f"""
```
Resending...

```
{question}
""",
        save=False,
    )

    # Replace the question
    user_message_json.text = question

    return user_message_json
