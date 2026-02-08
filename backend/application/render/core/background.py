import os
from PIL import Image, ImageDraw
from .render_setting import get_background_file
from application.config.paths import IMG_PATH
def load_background(character_ctx, template_size=(1340, 2159), background_image=None):
    # 讀圖
    if background_image is None:
        default_file = IMG_PATH / "background/default.png"
        background_file = get_background_file(character_ctx.en_name)
        if not os.path.exists(background_file):
            background_file = default_file
        background = Image.open(background_file).convert("RGBA")
    else:
        background = background_image.convert("RGBA")

    target_w, target_h = template_size
    img_w, img_h = background.size

    # cover 效果：保持比例 + 填滿
    scale = max(target_w / img_w, target_h / img_h)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    background = background.resize((new_w, new_h), resample=Image.LANCZOS)

    # 中心裁切
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    right = left + target_w
    bottom = top + target_h
    background = background.crop((left, top, right, bottom))

    # 半透明遮罩
    overlay = Image.new("RGBA", background.size, (0, 0, 0, 150))
    background = Image.alpha_composite(background, overlay)

    return background

def combine_background_template(background, template):
    return Image.alpha_composite(background, template)

def prepare_canvas_for_drawing(canvas):
    return ImageDraw.Draw(canvas)
