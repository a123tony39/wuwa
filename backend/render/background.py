from PIL import Image, ImageDraw

def load_background(background_file, width, height):
    background = Image.open(background_file).convert("RGBA")
    background = background.resize((width, height))
    background.putalpha(80)
    return background

def combine_background_template(background, template):
    return Image.alpha_composite(background, template)

def prepare_canvas_for_drawing(canvas):
    return ImageDraw.Draw(canvas)
