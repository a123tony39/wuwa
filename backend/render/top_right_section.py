from PIL import Image
from dataclasses import dataclass
from .core.canvas import paste_icon, draw_text
from .context import RenderContext

STAT_ROW_WIDTH = 500
STAT_ROW_HEIGHT = 70
TEXT_PADDING_RIGHT = 10
TEXT_Y_OFFSET = 17.5

@dataclass
class TopRightLayout:
    origin_x: int
    origin_y: int

def render_top_right_section(
        ctx: RenderContext,
        total_stats, 
        layout: TopRightLayout,
        sorted_allowed_stats, 
        FLAT_STATS,
    ):
    cnt = 0
    cursor_y = layout.origin_y
    for stat_name in sorted_allowed_stats:
        values = total_stats.get(stat_name, 0)
        print(f"{stat_name}:{values}")
        # paste img
        color = "white" if cnt % 2 == 0 else "gray"
        path = ctx.img_path / f"total_stat/{color}" / f"{ctx.stats_name_map[stat_name]}.png"
        img = Image.open(path)
        region = ctx.canvas.crop((layout.origin_x, cursor_y, layout.origin_x + img.width, cursor_y + img.height))
        composite = Image.alpha_composite(region, img)
        paste_icon(ctx.canvas, composite, (layout.origin_x, cursor_y))
        # paste value
        text = f"{values:.1f}%" if stat_name not in FLAT_STATS else f"{values[0]}".rstrip('0').rstrip('.')  + " / " + f"{values[1]:.1f}%"
        text_width = ctx.canvas_draw.textlength(text, font=ctx.fonts.stat(24))
        text_x = layout.origin_x + STAT_ROW_WIDTH - text_width - TEXT_PADDING_RIGHT
        text_y = cursor_y + TEXT_Y_OFFSET
        draw_text(ctx.canvas_draw, (text_x, text_y), text=text, font=ctx.fonts.stat(24),  fill = (255, 255, 255))
        # add cnt & move y
        cursor_y += STAT_ROW_HEIGHT
        cnt += 1

