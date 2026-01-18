from PIL import Image
from typing import Dict, Set
from dataclasses import dataclass
from domain.echo.ocr_parser import get_echo_info, EchoData
from domain.score.score import ECHO_SCORE_LEVELS, compute_echo_score
from domain.score.rules import ScoreRules
from domain.stats.rules import FLAT_STATS
from domain.ocr.ocr_result import OCRResult
from domain.character.context import CharacterContext
from .context import RenderContext
from .core.canvas import draw_text, paste_icon, add_border

@dataclass(frozen=True)
class main_stat_frame_size:
    width: int
    height: int
    
@dataclass
class EchoLayout:
    avatar_positions: list[tuple]
    stat_positions: list[tuple]
    main_stat_frame_size: main_stat_frame_size
    sub_stat_frame_width: int
    main_stat_top_offset: int
    avatar_main_stat_gap: int
    sub_stat_offset_from_main_stat: int
    sub_stat_x_offset_from_panel_origin: int
    
def render_echo_section(
    ctx: RenderContext,
    character: CharacterContext,
    layout: EchoLayout,
    rules: ScoreRules,
    source: Image.Image,
    total_stats: Dict[str, float],
    ocr_results: OCRResult,
):
    total_score = 0.0
    echo_results = []
    for idx, (ocr_result, avatar_pos, stat_pos) in enumerate(zip(ocr_results, layout.avatar_positions, layout.stat_positions)):
        print(f"--------聲骸評分{idx+1}--------")
        echo = get_echo_info(ocr_result)
        # calculate echo score
        echo_score, breakdown = compute_echo_score(echo, character, rules)
        add_echo_result(echo_results, idx, echo_score)
               
        total_score += echo_score
        # 聲骸頭像 paste echo img
        x, y = stat_pos
        padding_y = layout.main_stat_top_offset
        y += padding_y
        echo_img = paste_echo_img(
            avatar_pos = avatar_pos, 
            source = source, 
            paste_pos = (x, y),
            canvas = ctx.canvas,
        )
        # 聲骸主詞條 paste echo main stat
        paste_echo_main_stat(
            ctx = ctx,
            paste_pos = (x + layout.avatar_main_stat_gap + echo_img.width, y), 
            valid_stats = character.valid_stats,
            echo = echo, 
            total_stats = total_stats,
            main_stat_size = layout.main_stat_frame_size
        ) 
        # 聲骸副詞條 paste echo sub stat
        start_x = x + layout.sub_stat_x_offset_from_panel_origin
        start_y = y + layout.sub_stat_offset_from_main_stat
        y_bias = 0
        y_bias = paste_echo_sub_stats(
            ctx = ctx,
            start_pos = (start_x, start_y),
            y_bias = y_bias,
            breakdown = breakdown, 
            total_stats = total_stats, 
            valid_stats = character.valid_stats, 
            sub_stat_width = layout.sub_stat_frame_width
        )
        # 此聲骸評分
        draw_echo_sub_stats_score_text(
            ctx,
            start_pos = (start_x, start_y),
            y_bias = y_bias,
            echo_score = echo_score,
            sub_stat_width = layout.sub_stat_frame_width
        )
    return total_score, echo_results

def paste_echo_img(
    avatar_pos: tuple, 
    paste_pos: tuple, 
    source: Image.Image, 
    canvas: Image.Image
):
    x, y = paste_pos
    ICON_OPTICAL_X_OFFSET = 10
    ICON_OPTICAL_Y_OFFSET = 13
    source_echo_img_size = (210, 180)
    target_echo_img_size = (90, 100)
    cropped_x, cropped_y = avatar_pos
    echo_img = source.crop((cropped_x, cropped_y, cropped_x + source_echo_img_size[0], cropped_y + source_echo_img_size[1]))
    echo_img.thumbnail(target_echo_img_size)
    add_border(echo_img, color=(255, 255, 255, 160), width=1)
    paste_icon(canvas, echo_img, (x + ICON_OPTICAL_X_OFFSET, y + ICON_OPTICAL_Y_OFFSET))
    return echo_img

def paste_echo_sub_stats(
    ctx: RenderContext, 
    breakdown: list[tuple], 
    total_stats: Dict[str, float], 
    start_pos: tuple, 
    valid_stats: Set[str], 
    y_bias: int, 
    sub_stat_width: int
):
    TEXT_OPTICAL_Y_OFFSET = 12.5
    start_x, start_y = start_pos
    right_edge = start_x + sub_stat_width
    for stat_name, stat_value, _ in breakdown: 
        total_stats[stat_name] += stat_value
        y = start_y + y_bias
        # paste img 
        img = load_stat_img(ctx, stat_name, valid_stats, True)
        region = ctx.canvas.crop((start_x, y, start_x + img.width, y + img.height))
        composite = Image.alpha_composite(region, img)
        paste_icon(ctx.canvas, composite, (start_x, y))

        # paste value
        text = f"{stat_value}%" if stat_name not in FLAT_STATS else f"{stat_value}".rstrip('0').rstrip('.')
        text_width = ctx.canvas_draw.textlength(text, font=ctx.fonts.stat(24))
        x = right_edge - text_width - 3
        y = y + TEXT_OPTICAL_Y_OFFSET
        draw_text(ctx.canvas_draw, (x, y), text=text, font=ctx.fonts.stat(24), fill = (255, 255, 255))
        # move y
        y_bias += 50
    return y_bias

def paste_echo_main_stat(
    ctx: RenderContext, 
    paste_pos: tuple,
    echo: EchoData, 
    total_stats: Dict[str, float],  
    valid_stats: Set[str], 
    main_stat_size: tuple,
):
    paste_x, paste_y = paste_pos
    stat_name, stat_value = echo.main_stat.name, echo.main_stat.value
    main_stat_width, main_stat_height = main_stat_size.width,  main_stat_size.height
    for i in range(2):
        if i == 0:
            stat_name, stat_value = echo.main_stat.name, echo.main_stat.value
        elif i == 1:
            paste_y += 50
            stat_name, stat_value = echo.static_stat.name, echo.static_stat.value

        total_stats[stat_name] += stat_value
        # paste img
        img = load_stat_img(ctx, stat_name, valid_stats, False)
        img = img.crop((0, 0, main_stat_width, main_stat_height))
        region = ctx.canvas.crop((paste_x, paste_y, paste_x + img.width, paste_y + img.height))
        composite = Image.alpha_composite(region, img)
        paste_icon(ctx.canvas, composite, (paste_x, paste_y))

        # paste value
        text_right_edge_gap = 3
        text_optical_offset = 12.5
        right_edge = paste_x + main_stat_width
        text = f"{stat_value}%" if stat_name not in FLAT_STATS else f"{stat_value}".rstrip('0').rstrip('.')
        text_width = ctx.canvas_draw.textlength(text, font=ctx.fonts.stat(24))
        text_x = right_edge - text_width - text_right_edge_gap
        text_y = paste_y + text_optical_offset
        draw_text(ctx.canvas_draw, (text_x, text_y), text=text, font=ctx.fonts.stat(24), fill = (255, 255, 255))

def add_echo_result(echo_results: list, idx: int, echo_score: float):
    if echo_score >= ECHO_SCORE_LEVELS["PERFECT"]:
        message = "完美的聲骸!"
    elif echo_score >= ECHO_SCORE_LEVELS["GOOD"]:
        message = "表現出色"
    else:
        message = "建議加強此聲骸"
    
    echo_results.append({
        "name": f"聲骸{idx+1}",
        "score": echo_score,
        "message": message,
    })

def draw_echo_sub_stats_score_text(ctx: RenderContext, echo_score: float, start_pos: tuple, y_bias: int, sub_stat_width: int):
    start_x, start_y = start_pos
    text = f"聲骸評分: {echo_score:.2f}"
    text_width = ctx.canvas_draw.textlength(text, font=ctx.fonts.text(28))
    x = start_x + (sub_stat_width - text_width)//2
    y = start_y + y_bias + 5
    if echo_score >= ECHO_SCORE_LEVELS["PERFECT"]:
        fill = (220, 80, 80)
        stroke = (150, 30, 30, 120)
    elif echo_score >= ECHO_SCORE_LEVELS["GOOD"]:
        fill = (225, 185, 110) 
        stroke = (120, 95, 40)
    else:
        fill = (210, 210, 210)
        stroke = (125, 125, 125)

    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        draw_text(ctx.canvas_draw, (x+dx, y+dy), text, font=ctx.fonts.text(28), fill=stroke)
    draw_text(ctx.canvas_draw, (x, y), text=text, font=ctx.fonts.text(28), fill = fill)

def load_stat_img(ctx: RenderContext, stat_name: str, valid: Set[str], is_sub_stat: bool):
    folder = "sub_stat" if is_sub_stat else "main_stat"
    is_valid = "invalid" if stat_name not in valid else "valid"
    file = ctx.img_path / folder / is_valid / f"{ctx.stats_name_map[stat_name]}.png"
    img = Image.open(file)
    return img