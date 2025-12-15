from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import easyocr
import numpy as np
import os
from parsers.ocr_parser import parse_ocr_output
from scoring.score import get_score, get_rank,  get_character_zh_and_en_name,  get_valid_stats
import yaml

img_path = "../img"
background_file =  os.path.join(img_path, "background/Yuno.png")
template_file = os.path.join(img_path, "new_template.png")
ss_score_file = os.path.join(img_path, "SS_score.png")
s_score_file = os.path.join(img_path, "S_score.png")
a_score_file = os.path.join(img_path, "A_score.png")
b_score_file = os.path.join(img_path, "B_score.png")

source_file = os.path.join(img_path, "test_img/Chisa.png")
output_path = os.path.join(img_path, "output.png")
font_path = "../ttf/Cubic_11.ttf"


rank_images = {
    "SS": ss_score_file,
    "S": s_score_file,
    "A": a_score_file,
    "B": b_score_file
}

def load_yaml(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
    
def add_border(img, color, width):
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, img.width-1, img.height-1), outline = color, width=width)

    return img

def get_rank_pic(rank):
    if rank in rank_images:
        return Image.open(rank_images[rank])
    else:
        raise ValueError(f"{rank} is not valid ranking")


def get_stat_img(stat_name, valid, STATS_NAME_MAP):
    filepath = "invalid" if stat_name not in valid else "valid"
    img = Image.open(os.path.join(img_path, f"stat_img/{filepath}/{STATS_NAME_MAP[stat_name]}.png"))
    return img

if __name__ == '__main__':
    BASE_SCORE = load_yaml("./scoring/base_score.yaml")
    STATS_EXPECT_BIAS = load_yaml("./scoring/stats_expect_bias.yaml") 
    CHARACTER_TEMPLATE = load_yaml("./scoring/character_template.yaml")
    STATS_CATEGORIES = load_yaml("./scoring/stats_categories.yaml")
    STATS_NAME_MAP = load_yaml("./scoring/stats_name_map.yaml")
    
    crop_areas = [
        (0, 650, 380, 1050),
        (380, 650, 380*2, 1050),
        (380*2, 650, 380*3, 1050),
        (380*3, 650, 380*4, 1050),
        (380*4, 650, 380*5, 1050),
    ]
    
    under_panel_x, under_panel_y = 87, 1050
    upper_left_edge, under_left_edge = 401, 51
    paste_positions = [
        (under_panel_x + upper_left_edge, under_panel_y + 43), 
        (under_panel_x + upper_left_edge + 350, under_panel_y + 43), 
        (under_panel_x + under_left_edge, under_panel_y + 463),
        (under_panel_x + under_left_edge + 350, under_panel_y + 463),
        (under_panel_x + under_left_edge + 350*2, under_panel_y + 463),
    ]
    # input
    source = Image.open(source_file)
    # read template 
    template = Image.open(template_file).convert("RGBA")
    # background
    background = Image.open(background_file).convert("RGBA")
    background = background.resize((template.width, template.height))
    background.putalpha(140)
    # composite bg and template
    canvas = Image.alpha_composite(background, template)
    # create ocr reader
    reader = easyocr.Reader(['en', 'ch_tra'])  
    
    # template draw
    canvas_draw = ImageDraw.Draw(canvas)

    # paste character
    cropped = source.crop((0, 0, 280, 150))
    cropped_np = np.array(cropped)
    results = reader.readtext(cropped_np)
    _, character_name, prob  = results[0]
    character_zh_name, character_en_name = get_character_zh_and_en_name(character_name = character_name, character_template=CHARACTER_TEMPLATE)
    character_file = os.path.join(img_path, f"character_img/{character_en_name}.png")
    character_img = Image.open(character_file)
    character_img = character_img.resize((500, 700), Image.LANCZOS)
    character_img = add_border(character_img, color="black", width=3)
    canvas.paste(character_img, (80, 119), character_img)

    # process echos
    total_score = 0.0
    sub_stat_slot_width = 330
    valid = get_valid_stats(character_zh_name,  STATS_CATEGORIES, CHARACTER_TEMPLATE)
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
        echo_score, breakdown = get_score(
            echo = new_echo, 
            valid_stats = valid, 
            character_name = character_zh_name,
            base_score = BASE_SCORE,
            stats_expect_bias = STATS_EXPECT_BIAS
        )
        total_score += echo_score

        # paste echo img
        cropped_x, cropped_y = crop_area[0], crop_area[1]
        if idx == 0:
            cropped_x += 10
        echo_img = source.crop((cropped_x, cropped_y, cropped_x + 210, cropped_y + 180))
        echo_img.thumbnail((90, 100))
        add_border(echo_img, color=(255, 255, 255, 160), width=1)
        x, y = paste_pos
        canvas.paste(echo_img, (x + 10, y + 13))
        # paste echo main stat
        stat_name, stat_value = new_echo.main_stat.name, new_echo.main_stat.value
        right_edge = x + 20 + echo_img.width + 230
        ## top img
        x = x + 20 + echo_img.width
        img = get_stat_img(stat_name, valid, STATS_NAME_MAP)
        img = img.crop((0, 0, 230, 50))
        region = canvas.crop((x, y, x + img.width, y + img.height))
        composite = Image.alpha_composite(region, img)
        canvas.paste(composite, (x, y))
        canvas_draw.rectangle(
            (x, y, x + 230, y + 50),
            outline = (255, 255, 255),
            width = 1
        )
        ## top value
        text = f"{stat_value}%" if stat_name not in ["生命", "攻擊", "防禦"] else f"{stat_value}"
        font = ImageFont.truetype("../ttf/Philosopher-Bold.ttf", 24)

        text_width = canvas_draw.textlength(text, font=font)
        text_x = right_edge - text_width - 3
        text_y = y + 12.5
        canvas_draw.text((text_x, text_y), text=text, font=font, fill = (255, 255, 255))
        ## bottom img
        stat_name, stat_value = new_echo.static_stat.name, new_echo.static_stat.value
        y += 50
        img = get_stat_img(new_echo.static_stat.name, valid, STATS_NAME_MAP)
        img = img.crop((0, 0, 230, 50))
        region = canvas.crop((x, y, x + img.width, y + img.height))
        composite = Image.alpha_composite(region, img)
        canvas.paste(composite, (x, y))
        canvas_draw.rectangle(
            (x, y, x + 230, y + 50),
            outline = (255, 255, 255),
            width = 1
        )
        # bottom value
        text = f"{stat_value}%" if stat_name not in ["生命", "攻擊", "防禦"] else f"{stat_value}"
        font = ImageFont.truetype("../ttf/Philosopher-Bold.ttf", 24)
        text_width = canvas_draw.textlength(text, font=font)
        text_x = right_edge - text_width - 3
        text_y = y + 12.5
        canvas_draw.text((text_x, text_y), text=text, font=font, fill = (255, 255, 255))
        # paste echo sub stat
        y_bias = 0
        start_x, start_y = paste_pos
        start_x += 10
        start_y += 108
        right_edge = start_x + sub_stat_slot_width
        canvas_draw.rectangle(
            (start_x, start_y, start_x + 330, start_y + 250),
            outline = (255, 255, 255),
            width = 1
        )
        for stat_name, stat_value, stat_score in breakdown: 
            y = start_y + y_bias
            filepath = "invalid" if stat_name not in valid else "valid"
            # paste img 
            img = Image.open(os.path.join(img_path, f"stat_img/{filepath}/{STATS_NAME_MAP[stat_name]}.png"))
            region = canvas.crop((start_x, y, start_x + img.width, y + img.height))
            composite = Image.alpha_composite(region, img)
            canvas.paste(composite, (start_x, y))

            # paste value
            text = f"{stat_value}%" if stat_name not in ["生命", "攻擊", "防禦"] else f"{stat_value}"
            font = ImageFont.truetype("../ttf/Philosopher-Bold.ttf", 24)
 
            text_width = canvas_draw.textlength(text, font=font)
            x = right_edge - text_width - 3
            y = y + 12.5
            canvas_draw.text((x, y), text=text, font=font, fill = (255, 255, 255))
            # move y
            y_bias += 50
        
        text = f"聲骸評分: {echo_score:.2f}"
        font = ImageFont.truetype("../ttf/NotoSansTC-SemiBold.ttf", 28)
        text_width = canvas_draw.textlength(text, font=font)
        x = start_x + (sub_stat_slot_width - text_width)//2
        y = start_y + y_bias + 5
        if echo_score >= 20:
            fill = (128, 0, 32)
            stroke = (220, 180, 170)
        elif echo_score >= 15:
            fill = (225, 185, 110) 
            stroke = (120, 95, 40)
        else:
            fill = (210, 210, 210)
            stroke = (125, 125, 125)

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            canvas_draw.text((x+dx, y+dy), text, font=font, fill=stroke)
        canvas_draw.text((x, y), text=text, font=font, fill = fill)

    total_score = round(total_score, 2)
    rank = get_rank(total_score)
    # rank pic
    slot_x, slot_y = under_panel_x + 51 + 85, under_panel_y + 33 + 120
    slow_w, slot_h = 180, 180
    print(f"{rank}: {total_score}")
    rank_img = get_rank_pic(rank)
    img_w, img_h = rank_img.size
    mid_x = slot_x + (slow_w - img_w) // 2
    mid_y = slot_y + (slot_h - img_h) // 2
    canvas.paste(rank_img, (mid_x, mid_y), rank_img)
    # set text and font
    text_zh = f"練度評分:{total_score:.2f}".rstrip('0').rstrip('.')
    font_zh = ImageFont.truetype("../ttf/NotoSansTC-Bold.ttf", 36)
    # compute and align center
    w_zh = canvas_draw.textlength(text_zh, font=font_zh)
    total_width = w_zh 
    rank_img_center = mid_x + rank_img.width//2
    x = rank_img_center - total_width//2
    y = mid_y + rank_img.height + 10
    canvas_draw.text((x, y), text_zh, font=font_zh, fill=(220, 220, 220))

    # save the result
    canvas.save(output_path)