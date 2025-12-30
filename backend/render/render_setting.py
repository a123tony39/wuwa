from PIL import ImageFont
from backend_config.paths import IMG_PATH

RANK_FONT = ImageFont.truetype("../ttf/NotoSansTC-SemiBold.ttf", 28)
STAT_FONT = ImageFont.truetype("../ttf/Philosopher-Bold.ttf", 24)
TEMPLATE_FILE = IMG_PATH / "new_template.png"

def get_background_file(character_en_name):
    return IMG_PATH / f"../img/background/{character_en_name}.png"