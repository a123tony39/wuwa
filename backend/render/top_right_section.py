from PIL import Image
from dataclasses import dataclass
from .core.canvas import paste_icon, draw_text
from .context import RenderContext

@dataclass(frozen=True)
class stat_frame_size:
    width: int
    height: int

@dataclass
class TopRightLayout:
    origin_x: int
    origin_y: int
    stat_frame_size: stat_frame_size
    text_right_padding: int
    line_gap: float

def render_top_right_section(
        ctx: RenderContext,
        total_stats, 
        layout: TopRightLayout,
        sorted_allowed_stats, 
        FLAT_STATS,
    ):
    cnt = 0
    cursor_y = layout.origin_y
    stat_row_width, stat_row_height = layout.stat_frame_size.width, layout.stat_frame_size.height
    for stat_name in sorted_allowed_stats:
        color = "white" if cnt % 2 == 0 else "gray"
        img = get_stat_img(stat_name, ctx, color)
        paste_stat_img(ctx, layout, cursor_y, img)
        stat_values = total_stats.get(stat_name, 0)
        stat_text =  set_text(stat_name, stat_values, FLAT_STATS)
        text_pos = cal_text_pos(ctx, stat_text, layout, stat_row_width, cursor_y)
        draw_text(ctx.canvas_draw, text_pos, text=stat_text, font=ctx.fonts.stat(24),  fill = (255, 255, 255))
        cursor_y += stat_row_height
        cnt += 1

def get_stat_img(stat_name, ctx, color):
    path = ctx.img_path / f"total_stat/{color}" / f"{ctx.stats_name_map[stat_name]}.png"
    return Image.open(path)

def paste_stat_img(ctx, layout, cursor_y, img):
    region = ctx.canvas.crop((layout.origin_x, cursor_y, layout.origin_x + img.width, cursor_y + img.height))
    composite = Image.alpha_composite(region, img)
    paste_icon(ctx.canvas, composite, (layout.origin_x, cursor_y))

def cal_text_pos(ctx, stat_value, layout, stat_row_width, cursor_y):
    text_width = ctx.canvas_draw.textlength(stat_value, font=ctx.fonts.stat(24))
    text_x = layout.origin_x + stat_row_width - text_width - layout.text_right_padding
    text_y = cursor_y + layout.line_gap
    return (text_x, text_y)

def set_text(stat_name, values, FLAT_STATS):
    # 暴擊 10.5% 
    # 攻擊 150 / 11.6%
    if stat_name in FLAT_STATS:
        if isinstance(values, (list, tuple)) and len(values) >= 2:
            flat_str = str(values[0]).rstrip('0').rstrip('.') or '0'  # 防止 0 變空
            percent_str = f"{values[1]:.1f}%"
            text = flat_str + " / " + percent_str
        else:
            text = str(values)
    else:
        text = f"{values:.1f}%"
    
    return text
