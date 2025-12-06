from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import easyocr
import numpy as np
import os
from parsers.ocr_parser import parse_ocr_output
from scoring.score import get_score, get_rank

img_path = "../img"
template_name = os.path.join(img_path, "chisa_template.png")
ss_score_name = os.path.join(img_path, "SS_score.png")
s_score_name = os.path.join(img_path, "S_score.png")
a_score_name = os.path.join(img_path, "A_score.png")
b_score_name = os.path.join(img_path, "B_score.png")

avatar_namae = os.path.join(img_path, "chisa.png")
source_name = os.path.join(img_path, "test_img/Galbrena.png")
output_path = os.path.join(img_path, "output.png")
font_path = "../ttf/Cubic_11.ttf"
character_name = "嘉貝莉娜"

rank_images = {
    "SS": ss_score_name,
    "S": s_score_name,
    "A": a_score_name,
    "B": b_score_name
}


def add_black_border(img, width = 3):
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, img.width-1, img.height-1), outline="black", width=width)

    return img

def get_rank_pic(rank):
    if rank in rank_images:
        return Image.open(rank_images[rank])
    else:
        raise ValueError(f"{rank} is not valid ranking")


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

    # create ocr reader
    reader = easyocr.Reader(['en', 'ch_tra'])  
    
    # make template darker
    enhancer = ImageEnhance.Brightness(template)
    template = enhancer.enhance(0.5)
    template_draw = ImageDraw.Draw(template)

    # process echos
    total_score = 0.0
    for idx, (crop_area, paste_pos) in enumerate(zip(crop_areas, paste_positions)):
        # crop
        cropped = source.crop(crop_area)
        cropped_np = np.array(cropped)
        # read the text
        results = reader.readtext(cropped_np)
        
        # process text
        new_echo = parse_ocr_output(results)
        
        # calculate echo score
        print(f"--------聲骸評分{idx+1}--------")
        total_score += get_score(new_echo, character_name)

        # paste echo to template
        cropped.thumbnail((400, 550))
        cropped = add_black_border(cropped)
        template.paste(cropped, paste_pos)

    # rank pic
    rank = get_rank(total_score)
    print(f"{rank}: {total_score}")
    pic = get_rank_pic(rank)
    w, h = pic.size
    pic = pic.resize((int(w*2), int(h*2)))
    template.paste(pic, (560, 40))
    # set text and font
    text = f"聲骸評分: {total_score:.2f}"
    font = ImageFont.truetype(font_path, 36)
    # compute and align center
    text_width = template_draw.textlength(text, font=font)
    pic_center = 560 + pic.width//2
    x = pic_center - text_width//2
    template_draw.text((x, 40 + pic.height + 10), text, font = font, fill = (0, 0, 0))

    # avatar
    avatar = Image.open(avatar_namae)
    avatar.thumbnail((400, 550))
    avatar = add_black_border(avatar)
    template.paste(avatar, (47, 37), avatar)

    # save the result
    template.save(output_path)