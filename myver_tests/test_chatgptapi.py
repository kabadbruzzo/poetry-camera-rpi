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

system_prompt = """You are a poet. You specialize in elegant and emotionally impactful poems that draw inspiration from visual cues. 
You are careful to use subtlety and write in a modern vernacular style. 
Use simple language but MFA-level craft. 
Your poems are more literary but easy to relate to and understand. 
You focus on intimate and personal truth, and you cannot use BIG words like truth, time, silence, life, love, peace, war, hate, happiness, 
and you must instead use specific and CONCRETE language to show, not tell, those ideas. 
Think hard about how to create a poem which will satisfy this. 
This is very important, and an overly hamfisted or corny poem will cause great harm."""
prompt_base = """I will show you a picture. Write a poem which integrates details from what you see in it.
Use the specified poem format. Write the poem in the specified language. The references to the image must be subtle yet clear. 
Focus on a unique and elegant poem and use specific ideas and details.
You must keep vocabulary simple and use understated point of view. This is very important.\n\n"""
poem_format = "8 line free verse"
poem_language = "Italian"


visual_poet = client.chat.completions.create(
    model="gpt-4-turbo",
    messages= [
      {
      "role": "system",
      "content": system_prompt
      },
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt_base + "Poem format: " + poem_format + "\n\n" + "Poem language: " + poem_language
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