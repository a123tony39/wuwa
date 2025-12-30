from PIL import Image
from .core.canvas import paste_icon, draw_text
def render_top_right_section(
        font,
        canvas, 
        img_path,
        total_stats, 
        canvas_draw, 
        STATS_NAME_MAP, 
        stat_total_width, 
        stat_total_height, 
        stat_total_value_x, 
        stat_total_value_y, 
        sorted_allowed_stats, 
        FLAT_STATS,
    ):
    cnt = 0
    for stat_name in sorted_allowed_stats:
        values = total_stats.get(stat_name, 0)
        print(f"{stat_name}:{values}")
        # paste img
        color = "white" if cnt % 2 == 0 else "gray"
        path = img_path / f"total_stat/{color}" / f"{STATS_NAME_MAP[stat_name]}.png"
        img = Image.open(path)
        region = canvas.crop((stat_total_value_x, stat_total_value_y, stat_total_value_x + img.width, stat_total_value_y + img.height))
        composite = Image.alpha_composite(region, img)
        paste_icon(canvas, composite, (stat_total_value_x, stat_total_value_y))
        # paste value
        text = f"{values:.1f}%" if stat_name not in FLAT_STATS else f"{values[0]}".rstrip('0').rstrip('.')  + " / " + f"{values[1]:.1f}%"
        text_width = canvas_draw.textlength(text, font=font)
        text_x = stat_total_value_x + stat_total_width - text_width - 10
        text_y = stat_total_value_y + 17.5
        draw_text(canvas_draw, (text_x, text_y), text=text, font=font,  fill = (255, 255, 255))
        # add cnt & move y
        stat_total_value_y += stat_total_height
        cnt += 1

def merge_flat_and_percent_stats(total_stats, FLAT_STATS):
    for base_stat in FLAT_STATS:
        hp = total_stats[base_stat]
        hp_percent = total_stats[f"{base_stat}%"]
        total_stats[base_stat] = [hp, hp_percent]
        total_stats.pop(f"{base_stat}%", None)