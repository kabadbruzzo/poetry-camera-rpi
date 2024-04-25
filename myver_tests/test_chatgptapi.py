import openai

open.api_key = open("../api_chatgpt.txt", "r").read().strip("\n")

visual_poet = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages = [
        {"role": "user", "content":"Scrivi una poesia sulla luna." }
    ]
)

poem = visual_poet.choices[0].message.content

print(poem)