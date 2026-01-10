
from collections import defaultdict
from config.paths import IMG_PATH

from domain.stats.rules import stat_sort_key, normalize_stats, merge_flat_and_percent_stats, FLAT_STATS

from render.context import RenderContext, FontSet
from render.core.render_setting import TEMPLATE_FILE,  get_text_font, get_stat_font, get_background_file
from render.background import load_background, combine_background_template, prepare_canvas_for_drawing
from render.layout_config import ECHO_AVATAR_POSITIONS, PASTE_POSITIONS
from render.top_left_section import render_top_left_section
from render.echo_section import render_echo_section, EchoLayout
from render.top_right_section import render_top_right_section, TopRightLayout

from infrastructure.image_loader import load_img

def build_render_context(character_ctx, score_rules) -> RenderContext:
    fonts = FontSet(
        text = get_text_font,
        stat = get_stat_font,
    ) 
    background_file = get_background_file(character_ctx.en_name)
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
    return render_ctx

CHARACTER_IMG_X, CHARACTER_IMG_Y = 80, 119
def render_top_left_block(ctx, character, player_info):
    render_top_left_section(
        ctx = ctx,
        character = character,
        player_info = player_info,
        character_img_x = CHARACTER_IMG_X,
        character_img_y = CHARACTER_IMG_Y,
    )

def render_echo_block(render_ctx, character_ctx, score_rules, ocr_results, source):
    layout = EchoLayout(
        avatar_positions=ECHO_AVATAR_POSITIONS,
        paste_positions=PASTE_POSITIONS,
    )

    total_stats = defaultdict(float)
    total_score, echo_results = render_echo_section(
        ctx=render_ctx,
        character=character_ctx,
        layout=layout,
        rules=score_rules,
        source=source,
        total_stats=total_stats,
        ocr_results=ocr_results.echo_block,
    )

    return total_score, echo_results, total_stats

TOP_RIGHT_X = 737
TOP_RIGHT_OFFSET_FROM_CHARACTER = 50
def render_top_right_block(character_ctx, render_ctx, total_stats):
    total_stats = merge_flat_and_percent_stats(total_stats, FLAT_STATS)
    allowed_stats = normalize_stats(character_ctx.valid_stats, FLAT_STATS) | FLAT_STATS
    sorted_allowed_stats = sorted(allowed_stats, key = lambda x : stat_sort_key(x))

    top_right_layout = TopRightLayout(
        origin_x = TOP_RIGHT_X,
        origin_y = CHARACTER_IMG_Y + TOP_RIGHT_OFFSET_FROM_CHARACTER,
    )
    render_top_right_section(
        ctx = render_ctx,
        FLAT_STATS = FLAT_STATS,
        total_stats = total_stats, 
        layout = top_right_layout,
        sorted_allowed_stats = sorted_allowed_stats,
    )