# takeFrom picamera2 examples: capture_jpeg.py 
#!/usr/bin/python3

# Capture a JPEG while still running in the preview mode. When you
# capture to a file, the return value is the metadata for that image.

import time, requests, signal, os, replicate

from picamera2 import Picamera2, Preview
from gpiozero import LED, Button
from Adafruit_Thermal import *
from wraptext import *
from poetografo_functions import *
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

#load API keys from .env
load_dotenv()
openai_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
REPLICATE_API_TOKEN = os.environ['REPLICATE_API_TOKEN']

#instantiate printer
baud_rate = 9600 # REPLACE WITH YOUR OWN BAUD RATE
printer = Adafruit_Thermal('/dev/ttyS0', baud_rate, timeout=5)

#instantiate camera
picam2 = Picamera2()
# start camera
picam2.start()
time.sleep(2) # warmup period since first few frames are often poor quality

#instantiate buttons
shutter_button = Button(22) # REPLACE WTH YOUR OWN BUTTON PINS
power_button = Button(26, hold_time = 2) #REPLACE WITH YOUR OWN BUTTON PINS
led = LED(20)

## CONSTANTS
# prompts
system_prompt = """You are a poet. You specialize in elegant and emotionally impactful poems. 
You are careful to use subtlety and write in a modern vernacular style. 
Use high-school level English but MFA-level craft. 
Your poems are more literary but easy to relate to and understand. 
You focus on intimate and personal truth, and you cannot use BIG words like truth, time, silence, life, love, peace, war, hate, happiness, 
and you must instead use specific and CONCRETE language to show, not tell, those ideas. 
Think hard about how to create a poem which will satisfy this. 
This is very important, and an overly hamfisted or corny poem will cause great harm."""
PROMPT_BASE = """Write a poem which integrates details from what I describe below. 
Use the specified poem format. The references to the source material must be subtle yet clear. 
Focus on a unique and elegant poem and use specific ideas and details.
You must keep vocabulary simple and use understated point of view. This is very important.\n\n"""
POEM_FORMAT = "8 line free verse"
POEM_LANGUAGE = "Italian"

OPENAI_API_KEY = "SOME KEY"
IMAGE_SAVE_PATH = "SOME PATH"

#############################
# CORE PHOTO-TO-POEM FUNCTION
#############################
def take_photo_and_print_poem():
  # blink LED in a background thread
  led.blink()

  # Take photo & save it
  take_photo(IMAGE_SAVE_PATH)

  # FOR DEBUGGING: print metadata
  #print(metadata)

  # Close camera -- commented out because this can only happen at end of program
  # picam2.close()

  # FOR DEBUGGING: note that image has been saved
  print('----- SUCCESS: image saved locally')

  print_header(printer)

  #########################
  # Send saved image to API
  #########################

  poem = get_poem(
    image_path=IMAGE_SAVE_PATH,
    poem_language=POEM_LANGUAGE,
    poem_format=POEM_FORMAT,
    prompt_base=PROMPT_BASE
  )

  # print for debugging
  print('--------POEM BELOW-------')
  print(poem)
  print('------------------')

  print_poem(poem, printer)

  print_footer(printer)

  led.off()

  return


##############
# POWER BUTTON
##############
def shutdown():
  print('shutdown button held for 2s')
  print('shutting down now')
  led.off()
  os.system('sudo shutdown -h now')

################################
# For RPi debugging:
# Handle Ctrl+C script termination gracefully
# (Otherwise, it shuts down the entire Pi -- bad)
#################################
def handle_keyboard_interrupt(sig, frame):
  print('Ctrl+C received, stopping script')
  led.off()

  #weird workaround I found from rpi forum to shut down script without crashing the pi
  os.kill(os.getpid(), signal.SIGUSR1)

signal.signal(signal.SIGINT, handle_keyboard_interrupt)


#################
# Button handlers
#################
def handle_pressed():
  led.on()
  led.off()
  print("button pressed!")
  take_photo_and_print_poem()

def handle_held():
  print("button held!")
  shutdown()


################################
# LISTEN FOR BUTTON PRESS EVENTS
################################
shutter_button.when_pressed = take_photo_and_print_poem
power_button.when_held = shutdown

signal.pause()
