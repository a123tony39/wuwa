from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import easyocr
import numpy as np
import os



img_path = "../img"
template_name = os.path.join(img_path, "chisa_template.png")
avatar_namae = os.path.join(img_path, "chisa.png")
source_name = os.path.join(img_path, "input.png")
output_path = os.path.join(img_path, "output.png")

if __name__ == '__main__':
    crop_areas = [
        (0, 650, 380, 1050),
        (380, 650, 380*2, 1050),
        (380*2, 650, 380*3, 1050),
        (380*3, 650, 380*4, 1050),
        (380*4, 650, 380*5, 1050),
    ]

    paste_positions = [
        (1000, 40),
        (1440, 40),
        (560, 550),
        (1000, 550),
        (1440, 550)
    ]
    # image open
    source = Image.open(source_name)
    template = Image.open(template_name)
    reader = easyocr.Reader(['en', 'ch_tra'])  # 英文+中文
    
    enhancer = ImageEnhance.Brightness(template)
    template = enhancer.enhance(0.5)

    # crop
    for crop_area, paste_pos in zip(crop_areas, paste_positions):
        cropped = source.crop(crop_area)
        cropped_np = np.array(cropped)
        results = reader.readtext(cropped_np)
        
        for bbox, text, prob in results:
            print(f"文字: {text}, 信心指數: {prob:.2f}")

        cropped.thumbnail((400, 550))
        template.paste(cropped, paste_pos)

    avatar = Image.open(avatar_namae)
    avatar.thumbnail((400, 550))
    draw = ImageDraw.Draw(avatar)
    width = 3
    draw.rectangle((0, 0, avatar.width-1, avatar.height-1), outline="black", width=width)

    template.paste(avatar, (47, 37), avatar)
    template.save(output_path)