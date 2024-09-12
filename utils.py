from cat.convo.messages import Role


def filter_dot_commands(history):

    cleaned_history = []

    for turn in history:

        if turn["role"] == Role.AI:
            if turn["why"].input[0] == ".":
                continue

        if turn["role"] == Role.Human:
            if turn["message"][0] == ".":
                continue

        cleaned_history.append(turn)

    return cleaned_history
