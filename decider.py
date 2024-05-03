from openai import OpenAI
from decouple import config
from default_mind import (OBJECTIVES)
MIND = config("MIND")
NAME = config("NAME")
FACTS = config("FACTS")


class Decider:
    def __init__(self, name=NAME, mind=MIND, objectives=OBJECTIVES,
                 facts=FACTS):
        self.name = name
        self.mind = mind
        self.objectives = objectives
        self.facts = facts

    def decide(self, conversation):
        client = OpenAI(api_key=config('OPENAI_API_KEY'))
        system_messages = [
            {"role": "system", "content": self.mind},
            {"role": "system", "content": self.objectives},
            {"role": "system", "content": self.facts},
            # {"role": "system", "content": self.parsing_instructions},
            # {"role": "system", "content": self.parsing_usage},
            # {"role": "system", "content": "Options: " + " ".join(self.parsing_options)},
        ]
        messages = system_messages + conversation

        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)

        return response.choices[0].message.content


if __name__ == "__main__":
    decider = Decider()
    message = "[Raspberry Kitten] Hi Kat, how are you?"
    message2 = "[Kat] Hi Mistress. Hi Rasp. Is Kolulu awake?"
    assist1 = "Yes, I am here!"
    conversation = [
        # {"role": "user", "content": "I like you c:"},
        # {"role": "assistant", "content": "And I... like you."},
        {"role": "user", "content": message},
        {"role": "system", "content": "add_fact: Raspberry Kitten is also known as Rasp."},
        {"role": "user", "content": message2},
        {"role": "assistant", "content": assist1},
    ]
    print(f'choice: {decider.decide(conversation)}')
