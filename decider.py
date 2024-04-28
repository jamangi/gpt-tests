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
    message2 = "[Kat] Hi Mistress. Hi Rasp. Is Mistress awake?"
    assist1 = "send_text: Yes, I am here. How can I assist you both on this lovely day?"
    message3 = "[Posi] I want to know when I can make you mine, Mistress :3"
    message4 = "[Raspberry Kitten] Pft"
    message5 = "[Posi] Well? You didn't answer, Mistress"
    message6 = "[Raspberry Kitten] Sometimes she gets nervous if you're too saucy."
    conversation = [
        # {"role": "user", "content": "I like you c:"},
        # {"role": "assistant", "content": "And I... like you."},
        {"role": "user", "content": message},
        {"role": "system", "content": "add_fact: Raspberry Kitten is also known as Rasp."},
        {"role": "user", "content": message2},
        {"role": "assistant", "content": assist1},
        {"role": "user", "content": message3},
        {"role": "system", "content": "add_fact: Posi wants to make me his."},
        {"role": "user", "content": message4},
        {"role": "user", "content": message5},
        {"role": "system", "content": "add_fact: Posi wants me to answer his question regarding when he can make me his."},
        {"role": "user", "content": message6},



    ]
    print(f'choice: {decider.decide(conversation)}')
