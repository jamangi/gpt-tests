from openai import OpenAI
from decouple import config
from default_mind import (MIND, OBJECTIVES, FACTS, PARSING_INSTRUCTIONS,
                          PARSING_OPTIONS, PARSING_USAGE)


class SessionManager:
    def __init__(self, decider, conversation):
        self.decider = decider
        self.conversation = conversation

    def process_user_message(self, message):
        self.conversation.append({"role": "user", "content": message})
        choices = self.decider.decide(self.conversation)
        print(f'choices: {choices}')
        match choices.split(':'):
            case["do_nothing"] | ["send_text"] | ["send_emoji"] | ["do nothing"] | ["send text"] | ["send emoji"]:
                return None
            case [option, argument]:
                if option in PARSING_OPTIONS:
                    return eval(f'self.{option}("{argument}")')
                else:
                    return self.send_text(choices)
            case _:
                return self.send_text(choices)

    def process_bot_message(self, message):
        self.conversation.append({"role": "assistant", "content": message})

    def add_fact(self, fact):
        action = 'add_fact: ' + fact
        self.conversation.append({"role": "system", "content": action})
        print(action)

    def add_objective(self, objective):
        action = 'add_objective: ' + objective
        self.conversation.append({"role": "system", "content": action})
        print(action)

    def remove_fact(self, fact):
        pass

    def remove_objective(self, fact):
        pass

    def send_text(self, text):
        return text

    def send_emoji(self, text):
        return text

    def do_nothing(self, text=None):
        pass


