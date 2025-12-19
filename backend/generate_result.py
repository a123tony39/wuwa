import os
import yaml
import easyocr
from pathlib import Path
from collections import defaultdict
from PIL import Image, ImageFont

from parsers.input_processing import get_player_info
from scoring.score import get_character_zh_and_en_name, get_valid_stats

from render.background import load_background, combine_background_template, prepare_canvas_for_drawing
from render.top_left_section import render_top_left_section
from render.top_right_section import render_top_right_section, merge_flat_and_percent_stats
from render.echo_section import render_echo_section
from render.rank_section import paste_rank

def load_yaml(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
    
def stat_sort_key(stat_name: str):
    STAT_GROUP_PRIORITY = {
        "生命": (0, 0),  
        "攻擊": (0, 1),
        "防禦": (0, 2),
        "共鳴效率": (1, 0),
        "暴擊": (2, 0),
        "暴擊傷害": (2, 1),
    }

    if stat_name in STAT_GROUP_PRIORITY:
        return (*STAT_GROUP_PRIORITY[stat_name], 0)
    return (99, 0, len(stat_name))

def normalize_stats(valid_stats, flat_stats):
    flat_percent = {f"{s}%" for s in flat_stats}
    return valid_stats - flat_percent

def load_source_img(source_file):
    return Image.open(source_file)

def load_template_img(template_file):
    return Image.open(template_file).convert("RGBA")

def process_image(source_file, output_file, reader):
    img_path = "../img"
    IMG_PATH = Path(img_path)
    template_file = IMG_PATH / "new_template.png"
    stat_font = ImageFont.truetype("../ttf/Philosopher-Bold.ttf", 24)
    FLAT_STATS = {"生命", "攻擊", "防禦"}

    total_stats = defaultdict(float)
    BASE_SCORE = load_yaml("./scoring/base_score.yaml")
    STATS_NAME_MAP = load_yaml("./scoring/stats_name_map.yaml")
    STATS_CATEGORIES = load_yaml("./scoring/stats_categories.yaml")
    STATS_EXPECT_BIAS = load_yaml("./scoring/stats_expect_bias.yaml") 
    CHARACTER_TEMPLATE = load_yaml("./scoring/character_template.yaml")
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
    
    source = load_source_img(source_file)  
    template = load_template_img(template_file)

    user_info = get_player_info(source, reader)

    character_zh_name, character_en_name = get_character_zh_and_en_name(
        character_name = user_info["character_name"], 
        character_template=CHARACTER_TEMPLATE
    )
    background_file =  os.path.join(img_path, f"background/{character_en_name}.png")
    background = load_background(background_file, template.width, template.height)

    canvas = combine_background_template(background, template)
    canvas_draw = prepare_canvas_for_drawing(canvas)
    # 左上區塊
    character_img_x, character_img_y = 80, 119
    render_top_left_section(
        canvas = canvas, 
        img_path = IMG_PATH,
        user_info = user_info,
        canvas_draw = canvas_draw, 
        STATS_NAME_MAP = STATS_NAME_MAP, 
        character_img_x = character_img_x,
        character_img_y = character_img_y,
        character_zh_name = character_zh_name,
        character_en_name = character_en_name,
        CHARACTER_TEMPLATE = CHARACTER_TEMPLATE,
    )
    
    # 下方區塊(聲骸部分)
    sub_stat_width = 330
    valid_stats = get_valid_stats(character_zh_name,  STATS_CATEGORIES, CHARACTER_TEMPLATE)
    total_score = render_echo_section(
        canvas = canvas,
        reader = reader, 
        source = source,
        img_path = IMG_PATH,
        stat_font = stat_font, 
        crop_areas = crop_areas,
        BASE_SCORE = BASE_SCORE,
        FLAT_STATS = FLAT_STATS,
        total_stats = total_stats,
        canvas_draw = canvas_draw,
        valid_stats = valid_stats, 
        STATS_NAME_MAP = STATS_NAME_MAP,
        sub_stat_width = sub_stat_width,
        paste_positions = paste_positions,
        character_zh_name = character_zh_name,
        STATS_EXPECT_BIAS = STATS_EXPECT_BIAS,
    )
    
    # 右上區塊
    top_stat_total_gap = 50
    stat_total_width, stat_total_height = 500, 70
    stat_total_value_x, stat_total_value_y = 737, character_img_y + top_stat_total_gap
    merge_flat_and_percent_stats(total_stats, FLAT_STATS)
    allowed_stats = normalize_stats(valid_stats, FLAT_STATS) | FLAT_STATS
    sorted_allowed_stats = sorted(allowed_stats, key = lambda x : stat_sort_key(x))

    render_top_right_section(
        canvas = canvas, 
        font = stat_font,
        img_path = IMG_PATH,
        FLAT_STATS = FLAT_STATS,
        canvas_draw = canvas_draw, 
        total_stats =  total_stats, 
        STATS_NAME_MAP = STATS_NAME_MAP,
        stat_total_width = stat_total_width,
        stat_total_height = stat_total_height,
        stat_total_value_x = stat_total_value_x, 
        stat_total_value_y = stat_total_value_y, 
        sorted_allowed_stats = sorted_allowed_stats,
    )
    # 下方區塊(評級部分)
    paste_rank(
        canvas = canvas, 
        img_path = IMG_PATH,
        canvas_draw = canvas_draw,
        total_score = total_score, 
        under_panel_x = under_panel_x, 
        under_panel_y = under_panel_y, 
    )

    # save the result
    canvas.save(output_file)
    
if __name__ == "__main__":
    source_files = [
        "../img/input/Cartethyia.png",
        "../img/input/Chisa.png",
        "../img/input/Zani.png",
        "../img/input/Cantarella.png",
        "../img/input/Lupa.png",
    ]
    ocr_reader = easyocr.Reader(['en', 'ch_tra'])  

    for idx, src_file in enumerate(source_files, start=1):
        filename = os.path.basename(src_file)
        name = os.path.splitext(filename)[0] 
        output_file = f"../img/output/{name}.png"
        process_image(src_file, output_file, ocr_reader)
        print(f"處理完成: {output_file}")