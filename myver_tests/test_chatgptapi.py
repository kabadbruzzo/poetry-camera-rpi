from openai import OpenAI

client = OpenAI(
    api_key = open("../api_chatgpt.txt", "r").read().strip("\n")
)

visual_poet = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages = [
        {"role": "user", "content":"Scrivi una poesia sulla luna." }
    ]
)

poem = visual_poet.choices[0].message.content

print(poem)