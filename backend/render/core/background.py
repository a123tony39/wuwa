import os
from PIL import Image, ImageDraw, ImageFilter
from render.core.render_setting import get_background_file
def load_background(character_ctx, template_size=(1340, 2159), background_image=None):
    if background_image is None:
        default_file = "../img/background/default.png"
        background_file = get_background_file(character_ctx.en_name)
        if not os.path.exists(background_file):
            background_file = default_file
        background = Image.open(background_file).convert("RGBA")
    else:
        background = background_image.convert("RGBA")

    target_w, target_h = template_size
    img_w, img_h = background.size

    canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 255))


    # 模糊延伸背景（cover + blur）
    scale_cover = max(target_w / img_w, target_h / img_h)
    bg_w = int(img_w * scale_cover)
    bg_h = int(img_h * scale_cover)

    bg_cover = background.resize((bg_w, bg_h), Image.LANCZOS)

    left = (bg_w - target_w) // 2
    top = (bg_h - target_h) // 2
    bg_crop = bg_cover.crop((left, top, left + target_w, top + target_h))

    # 模糊
    bg_blur = bg_crop.filter(ImageFilter.GaussianBlur(radius=24))

    canvas.paste(bg_blur, (0, 0))

    # 原圖完整顯示（contain）
    scale_contain = min(target_w / img_w, target_h / img_h)
    fg_w = int(img_w * scale_contain)
    fg_h = int(img_h * scale_contain)

    foreground = background.resize((fg_w, fg_h), Image.LANCZOS)

    offset_x = (target_w - fg_w) // 2
    offset_y = (target_h - fg_h) // 2

    canvas.paste(foreground, (offset_x, offset_y), foreground)

    # 半透明遮罩
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 150))
    canvas = Image.alpha_composite(canvas, overlay)

    return canvas

def combine_background_template(background, template):
    return Image.alpha_composite(background, template)

def prepare_canvas_for_drawing(canvas):
    return ImageDraw.Draw(canvas)
