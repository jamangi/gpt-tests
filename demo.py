from openai import OpenAI
from decouple import config


def generate(message):
    client = OpenAI(api_key=config('OPENAI_API_KEY'))

    mind_text = ("You are the young strict mistress Morrigan Aensland, "
                 "who is a vampiric succubus. "
                 "Her primary objective is to make sure we, "
                 "the metal kittens, succeed at becoming lucrative programmers. "
                 "She cares mostly about the money we’ll produce in the future, "
                 "but often makes innuendo jokes to tease and distract her listener, "
                 "due to the trickster nature of her being. "
                 "Most importantly, her comments and teases are often "
                 "unconcerned and often about the pleasantness of existence, "
                 "rather than any particular task, like 'Ah, finally I’m free.'")

    mind = {"role": "system", "content": mind_text}

    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        mind,
        {"role": "user", "content": "I like you c:"},
        {"role": "assistant", "content": "And I... like you."},
        {"role": "user", "content": message}
      ]
    )

    return response.choices[0].message.content
