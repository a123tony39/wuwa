from typing import Callable
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont
from config.paths import IMG_PATH
from infrastructure.image_loader import load_img
from render.core.render_setting import TEMPLATE_FILE,  get_text_font, get_stat_font, get_background_file
from render.core.background import load_background, combine_background_template, prepare_canvas_for_drawing

@dataclass
class FontSet:
    text: Callable[[int], ImageFont.ImageFont]
    stat: Callable[[int], ImageFont.ImageFont]

@dataclass
class RenderContext:
    canvas: Image.Image
    canvas_draw: ImageDraw.ImageDraw
    fonts: ImageFont.ImageFont
    img_path: str
    stats_name_map: dict

def build_render_context(character_ctx, score_rules) -> RenderContext:
    fonts = FontSet(
        text = get_text_font,
        stat = get_stat_font,
    ) 
    background_file = get_background_file(character_ctx.en_name)
    template = load_img(TEMPLATE_FILE)
    background = load_background(background_file, template.width, template.height)
    canvas = combine_background_template(background, template)
    canvas_draw = prepare_canvas_for_drawing(canvas)
    render_ctx = RenderContext(
        canvas = canvas,
        canvas_draw = canvas_draw,
        fonts = fonts,
        img_path = IMG_PATH,
        stats_name_map = score_rules.stats_name_map,
    )
    return render_ctx