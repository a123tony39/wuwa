from PIL import Image
from typing import Set
from dataclasses import dataclass
from domain.score.score import ECHO_SCORE_LEVELS
from domain.stats.rules import FLAT_STATS
from domain.character.context import CharacterContext
from .context import RenderContext
from .core.canvas import draw_text, paste_icon, add_border
from application.score_calculator import CharacterSummary

@dataclass(frozen=True)
class AvatarSize:
    width: int
    height: int

@dataclass(frozen=True)
class MainStatFrameSize:
    width: int
    height: int
    
@dataclass
class EchoLayout:
    avatar_size: AvatarSize
    avatar_positions: list[tuple]
    avatar_main_stat_gap: int
    stat_positions: list[tuple]
    main_stat_frame_size: MainStatFrameSize
    main_stat_top_offset: int
    sub_stat_frame_width: int
    sub_stat_offset_from_main_stat: int
    sub_stat_x_offset_from_panel_origin: int

def render_echo_section(
    ctx: RenderContext,
    character: CharacterContext,
    character_summary: CharacterSummary, 
    layout: EchoLayout,
    source: Image.Image,
):  
    for echo_result, avatar_pos, stat_pos in zip(character_summary.echo_results, layout.avatar_positions, layout.stat_positions):
        # 聲骸頭像 paste echo img
        padding_y = layout.main_stat_top_offset
        x, y = stat_pos   
        y += padding_y
        paste_echo_img(
            avatar_size = layout.avatar_size,
            avatar_pos = avatar_pos, 
            source = source, 
            paste_pos = (x, y),
            canvas = ctx.canvas,
        )
        # 聲骸主詞條 paste echo main stat
        paste_echo_main_stat(
            ctx = ctx,
            paste_pos = (x + layout.avatar_main_stat_gap + layout.avatar_size.width, y), 
            valid_stats = character.valid_stats,
            main_stats_result_list = echo_result.main_stats_result_list, 
            main_stat_size = layout.main_stat_frame_size
        ) 
        # 聲骸副詞條 paste echo sub stat
        start_x = x + layout.sub_stat_x_offset_from_panel_origin
        start_y = y + layout.sub_stat_offset_from_main_stat
        sub_stat_last_offset = paste_echo_sub_stats(
            ctx = ctx,
            start_pos = (start_x, start_y),
            sub_stats_result_list = echo_result.sub_stats_result_list, 
            valid_stats = character.valid_stats, 
            sub_stat_width = layout.sub_stat_frame_width
        )
        # 單一聲骸評分
        text = f"聲骸評分: {echo_result.score:.2f}"
        text_width = ctx.canvas_draw.textlength(text, font=ctx.fonts.text(28))
        x = start_x + (layout.sub_stat_frame_width - text_width)//2
        y = start_y + sub_stat_last_offset + 5
        draw_echo_sub_stats_score_text(
            ctx,
            text = text,
            paste_pos = (x, y),
            echo_score = echo_result.score
        )

def paste_echo_img(
    avatar_size: AvatarSize,
    avatar_pos: tuple, 
    paste_pos: tuple, 
    source: Image.Image, 
    canvas: Image.Image
):
    x, y = paste_pos
    ICON_OPTICAL_X_OFFSET = 10
    ICON_OPTICAL_Y_OFFSET = 13
    source_echo_img_size = (210, 180)
    cropped_x, cropped_y = avatar_pos
    echo_img = source.crop((cropped_x, cropped_y, cropped_x + source_echo_img_size[0], cropped_y + source_echo_img_size[1]))
    echo_img.thumbnail((avatar_size.width, avatar_size.height))
    add_border(echo_img, color=(255, 255, 255, 160), width=1)
    paste_icon(canvas, echo_img, (x + ICON_OPTICAL_X_OFFSET, y + ICON_OPTICAL_Y_OFFSET))

def paste_echo_main_stat(
    ctx: RenderContext, 
    paste_pos: tuple,
    main_stats_result_list, 
    valid_stats: Set[str], 
    main_stat_size: tuple,
):
    paste_x, paste_y = paste_pos
    main_stat_width, main_stat_height = main_stat_size.width,  main_stat_size.height
    print("test:", main_stats_result_list)
    
    for i in range(2):
        stat_name, stat_value = main_stats_result_list[i].name, main_stats_result_list[i].value
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
        paste_y += 50

def paste_echo_sub_stats(
    ctx: RenderContext, 
    sub_stats_result_list: list[tuple], 
    start_pos: tuple, 
    valid_stats: Set[str], 
    sub_stat_width: int
):
    offset = 0
    TEXT_OPTICAL_Y_OFFSET = 12.5
    start_x, start_y = start_pos
    right_edge = start_x + sub_stat_width
    for stat_name, stat_value, _ in sub_stats_result_list:
        y = start_y + offset
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
        offset += 50
    return offset

def draw_echo_sub_stats_score_text(ctx: RenderContext, echo_score: float, paste_pos: tuple, text: str):
    x, y = paste_pos
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