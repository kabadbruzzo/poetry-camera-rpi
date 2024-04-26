from openai import OpenAI
from os import path
import base64

client = OpenAI(
    api_key = open(path.realpath("D:/poetry-camera-rpi/api_chatgpt_kiara.txt"), "r").read().strip("\n")
)

# Load image from local storage

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

image_path = "D:\poetry-camera-rpi\myver_tests\image.jpg"

base64_image = encode_image(image_path)

# Text query about the image

text_query = "Scrivi una poesia su questa immagine."


visual_poet = client.chat.completions.create(
    model="gpt-4-turbo",
    messages= [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": text_query
          },
          {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
          }
        ]
    }
    ]

)


poem = visual_poet.choices[0].message.content

print(poem)