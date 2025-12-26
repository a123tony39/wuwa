from PIL import Image, ImageFont
from .canvas import draw_text, paste_icon, add_border

def render_top_left_section(
        canvas, 
        img_path,
        user_info,
        canvas_draw, 
        STATS_NAME_MAP, 
        character_img_x,
        character_img_y,
        character_zh_name,
        character_en_name,
        CHARACTER_TEMPLATE,
    ):
    render_player_info(canvas, canvas_draw, user_info)
    paste_character_img(canvas, character_en_name, (character_img_x, character_img_y), img_path)
    text_x, text_y = draw_character_text(canvas_draw, character_zh_name, (character_img_x, character_img_y))
    paste_element_img(canvas, STATS_NAME_MAP, CHARACTER_TEMPLATE, character_zh_name, text_x, text_y, img_path)

def render_player_info(canvas, canvas_draw, user_info):
    player_name, uid = user_info["player_name"], user_info["uid"]
    font = ImageFont.truetype("../ttf/NotoSansTC-SemiBold.ttf", 16)
    text = f"玩家名稱: {player_name}\nUID: {uid}"
    draw_text(
        canvas_draw,
        (canvas.width - 12, canvas.height - 12),
        text=text,
        font=font,
        fill=(210, 210, 210),
        anchor = "rd",  # right-bottom
        align = "right",
        spacing = 1,
        stroke_width=1,
        stroke_fill=(60, 60, 60)
    )

def paste_character_img(canvas, character_en_name, pos, img_path):
    character_file = img_path / "character" / f"{character_en_name}.png"
    character_img = Image.open(character_file)
    character_img = character_img.resize((500, 700), Image.LANCZOS)
    character_img = add_border(character_img, color="black", width=1)
    paste_icon(canvas, character_img, pos)

def draw_character_text(canvas_draw, character_zh_name, pos):
    character_img_width, character_img_height = 500, 700
    text = f"{character_zh_name}"
    font = ImageFont.truetype("../ttf/NotoSansTC-SemiBold.ttf", 36)
    text_width = canvas_draw.textlength(text, font = font)
    text_x = pos[0] + (character_img_width - text_width)//2
    text_y = pos[1] + character_img_height + 10
    draw_text(canvas_draw, (text_x, text_y), text=text, font=font, fill = (210, 210, 210))
    return text_x, text_y

def paste_element_img(canvas, STATS_NAME_MAP, CHARACTER_TEMPLATE, character_zh_name, text_x, text_y, img_path):
    element_file = img_path / "element" / f"{STATS_NAME_MAP[CHARACTER_TEMPLATE[character_zh_name]['element']]}.png"
    img = Image.open(element_file)
    paste_icon(canvas, img, (int(text_x - img.width), text_y))