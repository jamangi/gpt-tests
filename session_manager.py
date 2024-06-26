from openai import OpenAI
from decouple import config


class SessionManager:
    def __init__(self, decider, conversation):
        self.decider = decider
        self.conversation = conversation

    def process_user_message(self, message):
        if len(self.conversation) > 10:
            self.conversation = self.conversation[-10:]
            self.compress_conversation()
        self.conversation.append({"role": "user", "content": message})
        reply = self.decider.decide(self.conversation)
        return self.send_text(reply)

    def process_bot_message(self, message):
        self.conversation.append({"role": "assistant", "content": message})

    def compress_conversation(self):
        client = OpenAI(api_key=config('OPENAI_API_KEY'))
        request = [
            {"role": "system", "content": "observe the following conversation history, "
                                          "and try to compress it all into a single comprehensive summary"},
        ]
        request.extend(self.conversation)
        request.append({"role": "system", "content": "Like I said, try to compress all that "
                                                     "into a single comprehensive summary. "
                                                     "Use the names mentioned in the history in your summary"})
        summary = client.chat.completions.create(model="gpt-3.5-turbo", messages=request)
        self.conversation = [{"role": "system", "content": summary.choices[0].message.content}]
        print(f'history summary: {summary.choices[0].message.content}')

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


