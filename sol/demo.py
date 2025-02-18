import os

from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'developer', 'content': 'You keep your responses short and straight to the point. You always start your response with \'I believe,\''},
        {'role': 'user', 'content': 'What is Cisco Packet Tracer?'}
    ],
    n=3
)

for choice in completion.choices:
    print(choice.message.content)

pass
