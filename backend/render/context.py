from typing import Callable
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont

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