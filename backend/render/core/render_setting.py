from PIL import ImageFont
from config.paths import IMG_PATH

TEMPLATE_FILE = IMG_PATH / "new_template.png"

def get_text_font(size: int):
    return ImageFont.truetype("../ttf/NotoSansTC-SemiBold.ttf", size)

def get_stat_font(size: int):
    return ImageFont.truetype("../ttf/Philosopher-Bold.ttf", size)

def get_background_file(character_en_name):
    return IMG_PATH / f"../img/background/{character_en_name}.png"