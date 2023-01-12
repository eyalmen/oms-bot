import requests
from nextcord import Embed
import random


def return_chunks(text, max_characters, delimiter):
    chunks = []

    if delimiter == "" or delimiter not in text:
        # Split the text into chunks of max_characters
        for i in range(0, len(text), max_characters):
            chunks.append(text[i:i+max_characters])

    else:
        text = text.split(delimiter)
        # go over the split text
        # add the text + the delimiter to the chunks list, a new chunk if the length of the chunk is bigger than max_characters else add to the last chunk
        for i in range(len(text)):
            if len(chunks) == 0:
                chunks.append(text[i] + delimiter)
            elif len(chunks[-1]) + len(text[i]) + len(delimiter) > max_characters:
                chunks.append(text[i] + delimiter)
            else:
                chunks[-1] += text[i] + delimiter
        
    return chunks

def format(text):
    return f"**{text.capitalize()}:**"

def is_valid_url(url):
    # check for header content-type starts with image
    # if it doesnt start with that or the status code is not 200, return False
    # else return True
    request = requests.get(url)
    if request.status_code == 200 and request.headers["content-type"].startswith("image"):
        return True
    return False

def get_ansi_color_codes():
    return  {
    "green": "\u001B[32m", # ansicolor green
    "red": "\u001B[31m", # ansicolor red
    "blue": "\u001B[34m", # ansicolor blue
    "white": "\u001B[37m", # ansicolor white
    "purple": "\u001B[35m", # ansicolor purple
    "yellow": "\u001B[33m", # ansicolor yellow
    "light yellow": "\u001B[93m", # ansicolor light yellow
    "cyan": "\u001B[36m", # ansicolor cyan
    "black": "\u001B[30m", # ansicolor black
    "light black": "\u001B[90m", # ansicolor light black
    "reset": "\u001B[0m" # ansicolor reset
}

def get_random_embed_side_colour(embed):
    sylveon_colour_scheme = ["76C2E3","8CD7F7","C1C1C1","F8F8F8","EA98B2","ED9DB6","FEB6CC","D6507A"] # blue to white to pink
    embed.colour = int(random.choice(sylveon_colour_scheme), 16)