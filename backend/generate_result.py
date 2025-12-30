import os
from pathlib import Path
from collections import defaultdict
from PIL import Image, ImageFont
from memory_profiler import profile

from parsers.input_processing import get_player_info

from render.background import load_background, combine_background_template, prepare_canvas_for_drawing
from render.top_left_section import render_top_left_section
from render.top_right_section import render_top_right_section, merge_flat_and_percent_stats
from render.echo_section import render_echo_section
from render.rank_section import paste_rank

from infrastructure.ocr.google_ocr import google_ocr
from infrastructure.config.loader import load_yaml

from domain.score.rules import ScoreRules
from domain.character.get_character_info import get_character_zh_and_en_name, get_valid_stats_and_role

def load_rules(domain_path: Path = Path("./domain")) -> ScoreRules:
    base_score = load_yaml(domain_path / "score" / "base_score.yaml")
    stats_name_map = load_yaml(domain_path / "stats" / "stats_name_map.yaml")
    stats_categories = load_yaml(domain_path / "stats" / "stats_categories.yaml")
    stats_expect_bias = load_yaml(domain_path / "stats" / "stats_expect_bias.yaml") 
    return ScoreRules(base_score, stats_name_map, stats_categories, stats_expect_bias)

def load_character_template(path = Path("./domain/character/character_template.yaml")):
    return load_yaml(path)
    
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

def process_image(source, debug=False):
    img_path = "../img"
    IMG_PATH = Path(img_path)
    template_file = IMG_PATH / "new_template.png"
    stat_font = ImageFont.truetype("../ttf/Philosopher-Bold.ttf", 24)
    FLAT_STATS = {"生命", "攻擊", "防禦"}
    total_stats = defaultdict(float)

    rules = load_rules()
    character_template = load_character_template()

    echo_avater_positions = [
        (0, 650),
        (380, 650),
        (380*2, 650),
        (380*3, 650),
        (380*4, 650),
    ]
    ocr_crop_areas = [
        (0, 0, 300, 150),
        (60, 710, 380, 1050),
        (440, 710, 380*2, 1050),
        (815, 710, 380*3, 1050),
        (1190, 710, 380*4, 1050),
        (1560, 710, 380*5, 1050),
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
    
    template = load_template_img(template_file)
    # google ocr
    ocr_results = google_ocr(source, ocr_crop_areas)
    user_info = get_player_info(ocr_results[0])

    character_zh_name, character_en_name = get_character_zh_and_en_name(
        character_name = user_info["character_name"], 
        character_template = character_template
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
        STATS_NAME_MAP = rules.stats_name_map, 
        character_img_x = character_img_x,
        character_img_y = character_img_y,
        character_zh_name = character_zh_name,
        character_en_name = character_en_name,
        CHARACTER_TEMPLATE = character_template,
    )
    
    # 下方區塊(聲骸部分)
    sub_stat_width = 330
    valid_stats, role = get_valid_stats_and_role(character_zh_name,  rules.stats_categories, character_template)
    total_score = render_echo_section(
        canvas = canvas,
        source = source,
        img_path = IMG_PATH,
        stat_font = stat_font, 
        echo_avater_positions = echo_avater_positions,
        FLAT_STATS = FLAT_STATS,
        total_stats = total_stats,
        canvas_draw = canvas_draw,
        valid_stats = valid_stats, 
        sub_stat_width = sub_stat_width,
        paste_positions = paste_positions,
        character_zh_name = character_zh_name,
        STATS_NAME_MAP = rules.stats_name_map,
        BASE_SCORE = rules.get_role_base_score(role),
        STATS_EXPECT_BIAS = rules.stats_expects_bias,
        ocr_results = ocr_results[1:]
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
        STATS_NAME_MAP = rules.stats_name_map,
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

    if debug:
        canvas.show()
    else:
        return {"text": "圖片處理完成", "image": canvas}

@profile
def main():
    source_files = [
        #"../img/input/Cartethyia.png",
        # "../img/input/Chisa.png",
        # "../img/input/Zani.png",
        # "../img/input/Cantarella.png",
        # "../img/input/Lupa.png",
        "../img/input/Changli.png",
    ]

    for _, src_file in enumerate(source_files, start=1):
        src = Image.open(src_file)
        process_image(src, debug=True)


if __name__ == "__main__":
    main()