from openai import OpenAI

gpt = OpenAI()

completion = gpt.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'developer', 'content': 'You are an experienced network engineer.'},
        {'role': 'user', 'content': 'Briefly list all OSPF LSA types.'}
    ],
    # n=3
    
)

for choice in completion.choices:
    print(choice.message.content)

pass