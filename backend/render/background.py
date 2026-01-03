import os
from PIL import Image, ImageDraw

def load_background(background_file, width, height):
    default_file = "../img/background/default.png"
    if not os.path.exists(background_file):
        background_file = default_file
    background = Image.open(background_file).convert("RGBA")
    background = background.resize((width, height), resample = Image.LANCZOS)

    overlay = Image.new("RGBA", background.size, (0, 0, 0, 150))
    background = Image.alpha_composite(background, overlay)
    return background

def combine_background_template(background, template):
    return Image.alpha_composite(background, template)

def prepare_canvas_for_drawing(canvas):
    return ImageDraw.Draw(canvas)
