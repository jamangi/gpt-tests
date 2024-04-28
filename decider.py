from openai import OpenAI
from decouple import config
from default_mind import (MIND, OBJECTIVES, FACTS, PARSING_INSTRUCTIONS,
                          PARSING_OPTIONS, PARSING_EXPLANATION, PARSING_USAGE)


class Decider:
    def __init__(self, mind=MIND, objectives=OBJECTIVES,
                 facts=FACTS, parsing_options=PARSING_OPTIONS,
                 parsing_explanation=PARSING_EXPLANATION,
                 parsing_usage=PARSING_USAGE):
        self.mind = mind
        self.objectives = objectives
        self.facts = facts
        self.parsing_instructions = PARSING_INSTRUCTIONS
        self.parsing_options = parsing_options
        self.parsing_explanation = parsing_explanation
        self.parsing_usage = PARSING_USAGE

    def decide(self, conversation):
        client = OpenAI(api_key=config('OPENAI_API_KEY'))
        system_messages = [
            {"role": "system", "content": self.mind},
            {"role": "system", "content": self.objectives},
            {"role": "system", "content": self.facts},
            {"role": "system", "content": self.parsing_instructions},
            {"role": "system", "content": self.parsing_explanation},
            {"role": "system", "content": self.parsing_usage},
            {"role": "system", "content": "Options: " + " ".join(self.parsing_options)},
        ]
        messages = system_messages + conversation

        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)

        return response.choices[0].message.content


if __name__ == "__main__":
    decider = Decider()
    message = "[Raspberry Kitten] Hi Kat, how are you?"
    message2 = "[Raspberry Kitten] Hi Mistress. I'm doing okay. You seem chipper today."
    conversation = [
        # {"role": "user", "content": "I like you c:"},
        # {"role": "assistant", "content": "And I... like you."},
        {"role": "user", "content": message},

        {"role": "system", "content": "add_fact: Raspberry Kitten's real name is Rasp."},
        {"role": "system", "content": "add_fact Kat is a female."},
        {"role": "assistant", "content": "It's always a pleasure to see you, Rasp. How are you feeling today?"},
        {"role": "user", "content": message2},

    ]
    print(f'choice: {decider.decide(conversation)}')
