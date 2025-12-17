from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import easyocr
import numpy as np
import os
from parsers.ocr_parser import parse_ocr_output
from scoring.score import get_score, get_rank,  get_character_zh_and_en_name,  get_valid_stats
import yaml
from collections import defaultdict


img_path = "../img"
background_file =  os.path.join(img_path, "background/Lupa.png")
template_file = os.path.join(img_path, "new_template.png")
ss_score_file = os.path.join(img_path, "score/SS_score.png")
s_score_file = os.path.join(img_path, "score/S_score.png")
a_score_file = os.path.join(img_path, "score/A_score.png")
b_score_file = os.path.join(img_path, "score/B_score.png")
f_score_file = os.path.join(img_path, "score/F_score.png")

stat_font = ImageFont.truetype("../ttf/Philosopher-Bold.ttf", 24)


FLAT_STATS = {"生命", "攻擊", "防禦"}

rank_images = {
    "SS": ss_score_file,
    "S": s_score_file,
    "A": a_score_file,
    "B": b_score_file,
    "F": f_score_file,
}

STAT_GROUP_PRIORITY = {
    "生命": (0, 0),  
    "攻擊": (0, 1),
    "防禦": (0, 2),
    "共鳴效率": (1, 0),
    "暴擊": (2, 0),
    "暴擊傷害": (2, 1),
}


def load_yaml(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
    
def add_border(img, color, width):
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, img.width-1, img.height-1), outline = color, width=width)

    return img

def process_echo_main_stat(paste_x, paste_y, canvas, canvas_draw, echo, total_stats,  valid_stats, STATS_NAME_MAP):
    main_stat_width, main_stat_height = 230, 50
    stat_name, stat_value = echo.main_stat.name, echo.main_stat.value
    
    for i in range(2):
        if i == 0:
            stat_name, stat_value = echo.main_stat.name, echo.main_stat.value
        elif i == 1:
            paste_y += 50
            stat_name, stat_value = echo.static_stat.name, echo.static_stat.value

        total_stats[stat_name] += stat_value
        # paste img
        img = get_stat_img(stat_name, valid_stats, STATS_NAME_MAP, False)
        img = img.crop((0, 0, main_stat_width, main_stat_height))
        region = canvas.crop((paste_x, paste_y, paste_x + img.width, paste_y + img.height))
        composite = Image.alpha_composite(region, img)
        canvas.paste(composite, (paste_x, paste_y))
        # paste value
        text_right_edge_gap = 3
        text_optical_offset = 12.5
        right_edge = paste_x + main_stat_width
        text = f"{stat_value}%" if stat_name not in FLAT_STATS else f"{stat_value}".rstrip('0').rstrip('.')
        text_width = canvas_draw.textlength(text, font=stat_font)
        text_x = right_edge - text_width - text_right_edge_gap
        text_y = paste_y + text_optical_offset
        canvas_draw.text((text_x, text_y), text=text, font=stat_font, fill = (255, 255, 255))

def get_rank_pic(rank):
    if rank in rank_images:
        return Image.open(rank_images[rank])
    else:
        raise ValueError(f"{rank} is not valid ranking")

def get_stat_img(stat_name, valid, STATS_NAME_MAP, is_sub_stat):
    folder = "sub_stat" if is_sub_stat else "main_stat"
    is_valid = "invalid" if stat_name not in valid else "valid"
    img = Image.open(os.path.join(img_path, f"{folder}/{is_valid}/{STATS_NAME_MAP[stat_name]}.png"))
    return img

def stat_sort_key(stat_name: str):
    if stat_name in STAT_GROUP_PRIORITY:
        return (*STAT_GROUP_PRIORITY[stat_name], 0)
    return (99, 0, len(stat_name))

def normalize_stats(valid_stats, flat_stats):
    flat_percent = {f"{s}%" for s in flat_stats}
    return valid_stats - flat_percent

def process_image(source_file, output_file):
    BASE_SCORE = load_yaml("./scoring/base_score.yaml")
    STATS_EXPECT_BIAS = load_yaml("./scoring/stats_expect_bias.yaml") 
    CHARACTER_TEMPLATE = load_yaml("./scoring/character_template.yaml")
    STATS_CATEGORIES = load_yaml("./scoring/stats_categories.yaml")
    STATS_NAME_MAP = load_yaml("./scoring/stats_name_map.yaml")
    total_stats = defaultdict(float)

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
    background.putalpha(80)
    # composite bg and template
    canvas = Image.alpha_composite(background, template)
    # create ocr reader
    reader = easyocr.Reader(['en', 'ch_tra'])  
    
    # template draw
    canvas_draw = ImageDraw.Draw(canvas)

    # paste character
    cropped = source.crop((0, 0, 300, 150))

    cropped = cropped.resize(
        (int(cropped.width*2), int(cropped.height*2)),
        resample=Image.NEAREST,
    )
    cropped = cropped.convert("L")
    cropped_np = np.array(cropped)
    results = reader.readtext(cropped_np)

    character_name, player_name, feature_code, excepting = None, None, None, None
    for _, text, prob in results:
        if character_name is None:
            character_name = text
        elif "玩家名稱" in text:
            colon_pos = text.find(":")
            if colon_pos != -1:
                player_name = text[colon_pos+1:].strip()
        elif "特徵碼" in text:
            colon_pos = text.find(":")
            if colon_pos != -1:
                uid = text[colon_pos+1:].strip()

    #  player name / feature code
    font = ImageFont.truetype("../ttf/NotoSansTC-SemiBold.ttf", 16)
    text = f"玩家名稱: {player_name}\nUID: {uid}"
    canvas_draw.text(
        (canvas.width - 12, canvas.height - 12),
        text=text,
        font=font,
        fill=(210, 210, 210),
        anchor = "rd",  # right-bottom
        align = "right",
        spacing = 1,
        stroke_width=1,
        stroke_fill=(60, 60, 60)
    )

    print(character_name, player_name, uid)
    # charcter img
    character_img_x, character_img_y = 80, 119
    character_zh_name, character_en_name = get_character_zh_and_en_name(character_name = character_name, character_template=CHARACTER_TEMPLATE)
    character_file = os.path.join(img_path, f"character/{character_en_name}.png")
    character_img = Image.open(character_file)
    character_img = character_img.resize((500, 700), Image.LANCZOS)
    character_img = add_border(character_img, color="black", width=3)
    canvas.paste(character_img, (character_img_x, character_img_y), character_img)
    # character name
    text = f"{character_zh_name}"
    font = ImageFont.truetype("../ttf/NotoSansTC-SemiBold.ttf", 36)
    text_width = canvas_draw.textlength(text, font = font)
    text_x = character_img_x + (character_img.width - text_width)//2
    text_y = character_img_y + character_img.height + 10
    canvas_draw.text((text_x, text_y), text=text, font=font, fill = (210, 210, 210))
    # element
    img = Image.open(os.path.join(img_path, f"element/{STATS_NAME_MAP[CHARACTER_TEMPLATE[character_zh_name]['element']]}.png"))
    canvas.paste(img, (int(text_x - img.width), text_y), img)
    # process echos
    total_score = 0.0
    sub_stat_slot_width = 330
    valid_stats = get_valid_stats(character_zh_name,  STATS_CATEGORIES, CHARACTER_TEMPLATE)
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
            valid_stats = valid_stats, 
            character_name = character_zh_name,
            base_score = BASE_SCORE,
            stats_expect_bias = STATS_EXPECT_BIAS
        )
        total_score += echo_score

        # 聲骸圖片 paste echo img 
        cropped_x, cropped_y = crop_area[0], crop_area[1]
        if idx == 0:
            cropped_x += 10
        echo_img = source.crop((cropped_x, cropped_y, cropped_x + 210, cropped_y + 180))
        echo_img.thumbnail((90, 100))
        add_border(echo_img, color=(255, 255, 255, 160), width=1)
        x, y = paste_pos
        canvas.paste(echo_img, (x + 10, y + 13))
        # 聲骸主詞條 paste echo main stat
        img_main_stat_gap = 20
        process_echo_main_stat(
            paste_x = x + img_main_stat_gap + echo_img.width, 
            paste_y = y, 
            canvas = canvas,
            canvas_draw = canvas_draw,
            valid_stats = valid_stats,
            echo = new_echo, 
            total_stats = total_stats,
            STATS_NAME_MAP = STATS_NAME_MAP
        ) 
        # 聲骸副詞條 paste echo sub stat
        y_bias = 0
        start_x, start_y = paste_pos
        start_x += 10
        start_y += 108
        right_edge = start_x + sub_stat_slot_width
        for stat_name, stat_value, stat_score in breakdown: 
            total_stats[stat_name] += stat_value
            y = start_y + y_bias
            # paste img 
            img = get_stat_img(stat_name, valid_stats, STATS_NAME_MAP, True)
            region = canvas.crop((start_x, y, start_x + img.width, y + img.height))
            composite = Image.alpha_composite(region, img)
            canvas.paste(composite, (start_x, y))

            # paste value
            text = f"{stat_value}%" if stat_name not in FLAT_STATS else f"{stat_value}".rstrip('0').rstrip('.')
            text_width = canvas_draw.textlength(text, font=stat_font)
            x = right_edge - text_width - 3
            y = y + 12.5
            canvas_draw.text((x, y), text=text, font=stat_font, fill = (255, 255, 255))
            # move y
            y_bias += 50
        
        text = f"聲骸評分: {echo_score:.2f}"
        font = ImageFont.truetype("../ttf/NotoSansTC-SemiBold.ttf", 28)
        text_width = canvas_draw.textlength(text, font=font)
        x = start_x + (sub_stat_slot_width - text_width)//2
        y = start_y + y_bias + 5
        if echo_score >= 20:
            fill = (220, 80, 80)
            stroke = (30, 30, 30)
        elif echo_score >= 15:
            fill = (225, 185, 110) 
            stroke = (120, 95, 40)
        else:
            fill = (210, 210, 210)
            stroke = (125, 125, 125)

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            canvas_draw.text((x+dx, y+dy), text, font=font, fill=stroke)
        canvas_draw.text((x, y), text=text, font=font, fill = fill)

    # 聲骸總數值(有效詞條) process and sorted stats's total 
    print(total_stats)
    for base_stat in FLAT_STATS:
        hp = total_stats[base_stat]
        hp_percent = total_stats[f"{base_stat}%"]
        total_stats[base_stat] = [hp, hp_percent]
        total_stats.pop(f"{base_stat}%", None)
    
    # paste stats's total value
    cnt = 0
    top_stat_total_gap = 50
    stat_total_width, stat_total_height = 500, 70
    stat_total_value_x, stat_total_value_y = 737, character_img_y + top_stat_total_gap
    allowed_stats = normalize_stats(valid_stats, FLAT_STATS) | FLAT_STATS
    sorted_allowed_stats = sorted(allowed_stats, key = lambda x : stat_sort_key(x))

    for stat_name in sorted_allowed_stats:
        values = total_stats.get(stat_name, 0)

        print(f"{stat_name}:{values}")
        # paste img
        color = "white" if cnt % 2 == 0 else "gray"
        img = Image.open(os.path.join(img_path, f"total_stat/{color}/{STATS_NAME_MAP[stat_name]}.png"))
        region = canvas.crop((stat_total_value_x, stat_total_value_y, stat_total_value_x + img.width, stat_total_value_y + img.height))
        composite = Image.alpha_composite(region, img)
        canvas.paste(composite, (stat_total_value_x, stat_total_value_y))
        # paste value
        text = f"{values:.1f}%" if stat_name not in FLAT_STATS else f"{values[0]}".rstrip('0').rstrip('.')  + " / " + f"{values[1]:.1f}%"
        text_width = canvas_draw.textlength(text, font=stat_font)
        text_x = stat_total_value_x + stat_total_width - text_width - 10
        text_y = stat_total_value_y + 17.5
        canvas_draw.text((text_x, text_y), text=text, font=stat_font,  fill = (255, 255, 255))
        # add cnt & move y
        stat_total_value_y += stat_total_height
        cnt += 1
            
    # total_score = round(total_score, 2)
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
    rank_img_center = mid_x + rank_img.width//2
    x = rank_img_center - w_zh//2
    y = mid_y + rank_img.height + 10
    canvas_draw.text((x, y), text_zh, font=font_zh, fill=(220, 220, 220))

    # save the result
    canvas.save(output_file)


if __name__ == "__main__":
    source_files = [
        # "../img/input/Cartethyia.png",
        # "../img/input/Chisa.png",
        "../img/input/Zeni.png",
        # "../img/input/Cantarella.png",
        # "../img/input/Lupa.png",
    ]

    for idx, src_file in enumerate(source_files, start=1):
        filename = os.path.basename(src_file)
        name = os.path.splitext(filename)[0] 
        output_file = f"../img/output/{name}.png"
        process_image(src_file, output_file)
        print(f"處理完成: {output_file}")