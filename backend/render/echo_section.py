from PIL import Image

from parsers.ocr_parser import parse_ocr_output
from domain.score.score import get_score
from .core.canvas import draw_text, paste_icon, add_border

from backend_config.paths import IMG_PATH
from .core.render_setting import STAT_FONT, RANK_FONT

def render_echo_section(
        canvas,
        source,
        echo_avater_positions,
        canvas_draw,
        valid_stats, 
        paste_positions,
        character_zh_name,
        BASE_SCORE,
        STATS_EXPECT_BIAS,
        total_stats,
        STATS_NAME_MAP,
        sub_stat_width,
        FLAT_STATS,
        ocr_results,
    ):
    total_score = 0.0
    for idx, (ocr_result, avatar_pos, paste_pos) in enumerate(zip(ocr_results, echo_avater_positions, paste_positions)):
        new_echo = get_new_echo(ocr_result)
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
        x, y = paste_pos
        echo_img = paste_echo_img(
            idx = idx,
            avatar_pos = avatar_pos, 
            source = source, 
            x = x,
            y = y,
            canvas = canvas,
        )
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
            STATS_NAME_MAP = STATS_NAME_MAP,
            FLAT_STATS = FLAT_STATS,
        ) 
        # 聲骸副詞條 paste echo sub stat
        start_x, start_y = paste_pos
        start_x += 10
        start_y += 108
        y_bias = 0
        right_edge = start_x + sub_stat_width
        y_bias = process_echo_sub_stats(
            canvas = canvas,
            canvas_draw = canvas_draw,
            start_x = start_x,
            start_y = start_y,
            y_bias = y_bias,
            right_edge = right_edge,
            breakdown = breakdown, 
            total_stats = total_stats, 
            valid_stats = valid_stats, 
            STATS_NAME_MAP = STATS_NAME_MAP, 
            FLAT_STATS = FLAT_STATS,
        )
        # 此聲骸評分
        draw_echo_sub_stats_score_text(
            canvas_draw = canvas_draw,
            start_x = start_x,
            start_y = start_y,
            y_bias = y_bias,
            echo_score = echo_score,
            sub_stat_slot_width = sub_stat_width,
        )
    return total_score

def get_new_echo(results):
    new_echo = parse_ocr_output(results)
    return new_echo

def paste_echo_img(idx, avatar_pos, source, x, y, canvas):
    cropped_x, cropped_y = avatar_pos
    if idx == 0:
        cropped_x += 10
    echo_img = source.crop((cropped_x, cropped_y, cropped_x + 210, cropped_y + 180))
    echo_img.thumbnail((90, 100))
    add_border(echo_img, color=(255, 255, 255, 160), width=1)
    paste_icon(canvas, echo_img, (x + 10, y + 13))
    return echo_img

def process_echo_sub_stats(breakdown, total_stats, start_x, start_y, valid_stats, STATS_NAME_MAP, canvas, canvas_draw, right_edge, y_bias, FLAT_STATS):
    for stat_name, stat_value, _ in breakdown: 
        total_stats[stat_name] += stat_value
        y = start_y + y_bias
        # paste img 
        img = load_stat_img(stat_name, valid_stats, STATS_NAME_MAP, True, IMG_PATH)
        region = canvas.crop((start_x, y, start_x + img.width, y + img.height))
        composite = Image.alpha_composite(region, img)
        paste_icon(canvas, composite, (start_x, y))

        # paste value
        text = f"{stat_value}%" if stat_name not in FLAT_STATS else f"{stat_value}".rstrip('0').rstrip('.')
        text_width = canvas_draw.textlength(text, font=STAT_FONT)
        x = right_edge - text_width - 3
        y = y + 12.5
        draw_text(canvas_draw, (x, y), text=text, font=STAT_FONT, fill = (255, 255, 255))
        # move y
        y_bias += 50
    return y_bias

def process_echo_main_stat(paste_x, paste_y, canvas, canvas_draw, echo, total_stats,  valid_stats, STATS_NAME_MAP, FLAT_STATS):
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
        img = load_stat_img(stat_name, valid_stats, STATS_NAME_MAP, False, IMG_PATH)
        img = img.crop((0, 0, main_stat_width, main_stat_height))
        region = canvas.crop((paste_x, paste_y, paste_x + img.width, paste_y + img.height))
        composite = Image.alpha_composite(region, img)
        paste_icon(canvas, composite, (paste_x, paste_y))

        # paste value
        text_right_edge_gap = 3
        text_optical_offset = 12.5
        right_edge = paste_x + main_stat_width
        text = f"{stat_value}%" if stat_name not in FLAT_STATS else f"{stat_value}".rstrip('0').rstrip('.')
        text_width = canvas_draw.textlength(text, font=STAT_FONT)
        text_x = right_edge - text_width - text_right_edge_gap
        text_y = paste_y + text_optical_offset
        draw_text(canvas_draw, (text_x, text_y), text=text, font=STAT_FONT, fill = (255, 255, 255))


def draw_echo_sub_stats_score_text(echo_score, start_x, start_y, canvas_draw, sub_stat_slot_width, y_bias):
    text = f"聲骸評分: {echo_score:.2f}"
    text_width = canvas_draw.textlength(text, font=RANK_FONT)
    x = start_x + (sub_stat_slot_width - text_width)//2
    y = start_y + y_bias + 5
    if echo_score >= 20:
        fill = (220, 80, 80)
        stroke = (150, 30, 30, 120)
    elif echo_score >= 15:
        fill = (225, 185, 110) 
        stroke = (120, 95, 40)
    else:
        fill = (210, 210, 210)
        stroke = (125, 125, 125)

    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        draw_text(canvas_draw, (x+dx, y+dy), text, font=RANK_FONT, fill=stroke)
    draw_text(canvas_draw, (x, y), text=text, font=RANK_FONT, fill = fill)

def load_stat_img(stat_name, valid, STATS_NAME_MAP, is_sub_stat, img_path):
    folder = "sub_stat" if is_sub_stat else "main_stat"
    is_valid = "invalid" if stat_name not in valid else "valid"
    file = img_path / folder / is_valid / f"{STATS_NAME_MAP[stat_name]}.png"
    img = Image.open(file)
    return img