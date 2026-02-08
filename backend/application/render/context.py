from typing import Callable
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont
from application.config.paths import IMG_PATH
from infrastructure.image_loader import load_img
from .core.render_setting import TEMPLATE_FILE,  get_text_font, get_stat_font
from .core.background import load_background, combine_background_template, prepare_canvas_for_drawing

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

def build_render_context(character_ctx, score_rules, background_image) -> RenderContext:
    fonts = FontSet(
        text = get_text_font,
        stat = get_stat_font,
    )
    template = load_img(TEMPLATE_FILE)
    background = load_background(character_ctx, (template.width, template.height), background_image)
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