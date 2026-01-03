from PIL import Image
from pathlib import Path
from collections import defaultdict
from memory_profiler import profile

from config.paths import IMG_PATH

from render.context import RenderContext, FontSet
from render.core.render_setting import TEMPLATE_FILE,  get_text_font, get_stat_font, get_background_file
from render.layout_config import ECHO_AVATAR_POSITIONS, OCR_CROP_AREAS, PASTE_POSITIONS
from render.background import load_background, combine_background_template, prepare_canvas_for_drawing
from render.top_right_section import render_top_right_section, TopRightLayout
from render.top_left_section import render_top_left_section
from render.echo_section import render_echo_section, EchoLayout
from render.rank_section import paste_rank

from infrastructure.ocr.google_ocr import GoogleOCR
from infrastructure.yaml_config.yaml import load_yaml
from infrastructure.image.loader import load_img

from domain.score.rules import ScoreRules
from domain.stats.rules import stat_sort_key, normalize_stats, merge_flat_and_percent_stats, FLAT_STATS
from domain.character.get_character_info import get_character_zh_and_en_name, get_valid_stats_and_role
from domain.character.context import CharacterContext
from domain.player.context import get_player_info

def load_score_rules(domain_path: Path = Path("./domain")) -> ScoreRules:
    base_score = load_yaml(domain_path / "score" / "base_score.yaml")
    stats_name_map = load_yaml(domain_path / "stats" / "stats_name_map.yaml")
    stats_categories = load_yaml(domain_path / "stats" / "stats_categories.yaml")
    stats_expect_bias = load_yaml(domain_path / "stats" / "stats_expect_bias.yaml") 
    return ScoreRules(base_score, stats_name_map, stats_categories, stats_expect_bias)

def load_character_template(path = Path("./domain/character/character_template.yaml")):
    return load_yaml(path)
    
def process_image(source, debug=False):
    # do ocr
    ocr_engine = GoogleOCR("config.json")
    ocr_results = ocr_engine.ocr(source, OCR_CROP_AREAS)

    # 初始化
    total_stats = defaultdict(float)
    score_rules = load_score_rules()
    character_template = load_character_template()
    fonts = FontSet(
        text = get_text_font,
        stat = get_stat_font,
    ) 
    player_info = get_player_info(ocr_results.player_block)
    character_zh_name, character_en_name = get_character_zh_and_en_name(
        character_name = player_info.character_name, 
        character_template = character_template
    )
    valid_stats, role = get_valid_stats_and_role(character_zh_name, score_rules.stats_categories, character_template)
    character_ctx = CharacterContext(
        zh_name = character_zh_name,
        en_name = character_en_name,
        template = character_template,
        valid_stats = valid_stats,
        role = role,
    )
    background_file = get_background_file(character_en_name)
    template = load_img(TEMPLATE_FILE)
    background = load_background(background_file, template.width, template.height)
    canvas = combine_background_template(background, template)
    canvas_draw = prepare_canvas_for_drawing(canvas)
    render_ctx = RenderContext(
        canvas = canvas,
        canvas_draw = canvas_draw,
        fonts = fonts,
        img_path = IMG_PATH,
        stats_name_map = score_rules.stats_name_map,
    )
    # 左上區塊
    character_img_x, character_img_y = 80, 119
    render_top_left_section(
        ctx = render_ctx,
        character = character_ctx,
        player_info = player_info,
        character_img_x = character_img_x,
        character_img_y = character_img_y,
    )
    # 下方區塊(聲骸部分)
    echo_layout = EchoLayout(
        avatar_positions=ECHO_AVATAR_POSITIONS,
        paste_positions=PASTE_POSITIONS
    )
    total_score = render_echo_section(
        ctx = render_ctx,
        character = character_ctx,
        layout = echo_layout,
        rules = score_rules,
        source = source,
        total_stats = total_stats,
        ocr_results = ocr_results.echo_block
    )
    # 右上區塊
    TOP_RIGHT_X = 737
    TOP_RIGHT_OFFSET_FROM_CHARACTER = 50
    total_stats = merge_flat_and_percent_stats(total_stats, FLAT_STATS)
    allowed_stats = normalize_stats(valid_stats, FLAT_STATS) | FLAT_STATS
    sorted_allowed_stats = sorted(allowed_stats, key = lambda x : stat_sort_key(x))

    top_right_layout = TopRightLayout(
        origin_x = TOP_RIGHT_X,
        origin_y = character_img_y + TOP_RIGHT_OFFSET_FROM_CHARACTER,
    )
    render_top_right_section(
        ctx = render_ctx,
        FLAT_STATS = FLAT_STATS,
        total_stats = total_stats, 
        layout = top_right_layout,
        sorted_allowed_stats = sorted_allowed_stats,
    )
    # 下方區塊(評級部分)
    paste_rank(
        ctx = render_ctx,
        total_score = total_score, 
    )

    return canvas.show() if debug else {"text": "圖片處理完成", "image": canvas}

@profile
def main():
    source_files = [
        # "../img/input/Cartethyia.png",
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