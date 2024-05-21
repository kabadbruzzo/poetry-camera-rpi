from openai import OpenAI
import os
import base64
from wraptext import *
import datetime
import time

def save_api_key(api_key_file_path):
    """For use during setup."""
    api_key = open(os.path.realpath(api_key_file_path), "r").read().strip("\n")
    os.environ["OPENAI_API_KEY"] = api_key

def take_photo(save_image_path):
    #instantiate camera
    picam2 = Picamera2()

    # start camera
    picam2.start()
    time.sleep(2) # warmup period since first few frames are often poor quality

    metadata = picam2.capture_file(save_image_path)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def get_prompt(poem_language = 'Italian', poem_format = '8 line free verse', prompt_base = ''):
    prompt = prompt_base + "Poem format: " + poem_format + "\n\n" + "Poem language: " + poem_language
    return prompt

def get_poem(image_path, poem_language, poem_format, prompt_base):

    client = OpenAI(api_key = OPENAI_API_KEY) ## API key should be a global variable in main script

    base64_image = encode_image(image_path)

    # Load image from local storage

    visual_poet = client.chat.completions.create(
        model="gpt-4-turbo",
        messages= [
        {
        "role": "system",
        "content": system_prompt ## system prompt should be a global variable in main script
        },
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": get_prompt(poem_language = poem_language, poem_format = poem_format, prompt_base = prompt_base)
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

    return(poem)

def print_header(printer):
    # Get current date+time -- will use for printing and file naming
    now = datetime.now()

    # Format printed datetime like:
    # Jan 1, 2023
    # 8:11 PM
    printer.justify('C') # center align header text
    date_string = now.strftime('%b %-d, %Y')
    time_string = now.strftime('%-I:%M %p')
    printer.println('\n')
    printer.println(date_string)
    printer.println(time_string)

    # optical spacing adjustments
    printer.setLineHeight(56) # I want something slightly taller than 1 row
    printer.println()
    printer.setLineHeight() # Reset to default (32)

    printer.println("`'. .'`'. .'`'. .'`'. .'`'. .'`")
    printer.println("   `     `     `     `     `   ")

def print_footer(printer):
    printer.justify('C') # center align footer text
    printer.println("   .     .     .     .     .   ")
    printer.println("_.` `._.` `._.` `._.` `._.` `._")
    printer.println('\n')
    printer.println(' This poem was written by AI.')
    printer.println()
    printer.println('Credits go to')
    printer.println('poetry.camera')
    printer.println('\n\n\n\n')

def print_poem(poem):
    #instantiate printer
    baud_rate = 9600 # REPLACE WITH YOUR OWN BAUD RATE
    printer = Adafruit_Thermal('/dev/ttyS0', baud_rate, timeout=5)

    # print for debugging
    print('--------POEM BELOW-------')
    print(poem)
    print('------------------')

    # wrap text to 32 characters per line (max width of receipt printer)
    printable_poem = wrap_text(poem, 32)

    print_header(printer)

    printer.justify('L') # left align poem text
    printer.println(printable_poem)

    print_footer(printer)

