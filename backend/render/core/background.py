import os
from PIL import Image, ImageDraw
from render.core.render_setting import get_background_file
def load_background(character_ctx, template_size, background_image=None):
    if background_image is None:
        default_file = "../img/background/default.png"
        background_file = get_background_file(character_ctx.en_name)
        if not os.path.exists(background_file):
            background_file = default_file
        background = Image.open(background_file).convert("RGBA")
    else:
        background = background_image
    background = background.resize(template_size, resample = Image.LANCZOS)
    overlay = Image.new("RGBA", background.size, (0, 0, 0, 150))
    background = Image.alpha_composite(background, overlay)
    return background

def combine_background_template(background, template):
    return Image.alpha_composite(background, template)

def prepare_canvas_for_drawing(canvas):
    return ImageDraw.Draw(canvas)
