from PIL import Image
from .core.canvas import draw_text, paste_icon, add_border
from .context import RenderContext
from domain.character.context import CharacterContext
from domain.player.context import PlayerInfo

def render_top_left_section(
        ctx: RenderContext,
        character: CharacterContext,
        player_info: PlayerInfo,
        character_img_x,
        character_img_y,
    ):
    render_player_info(ctx, player_info)
    paste_character_img(ctx, character, (character_img_x, character_img_y))
    text_x, text_y = draw_character_text(ctx, character, (character_img_x, character_img_y))
    paste_element_img(ctx, character, text_x, text_y)

def render_player_info(ctx: RenderContext, player_info: PlayerInfo):
    text = f"玩家名稱: {player_info.player_name}\nUID: {player_info.uid}"
    draw_text(
        ctx.canvas_draw,
        (ctx.canvas.width - 12, ctx.canvas.height - 12),
        text=text,
        font=ctx.fonts.text(16),
        fill=(210, 210, 210),
        anchor = "rd",  # right-bottom
        align = "right",
        spacing = 1,
        stroke_width=1,
        stroke_fill=(60, 60, 60)
    )

def paste_character_img(ctx: RenderContext, character: CharacterContext, pos):
    character_file = ctx.img_path / "character" / f"{character.en_name}.png"
    character_img = Image.open(character_file)
    character_img = character_img.resize((500, 700), Image.LANCZOS)
    character_img = add_border(character_img, color="black", width=1)
    paste_icon(ctx.canvas, character_img, pos)

def draw_character_text(ctx: RenderContext, character: CharacterContext, pos):
    character_img_width, character_img_height = 500, 700
    text = f"{character.zh_name}"
    text_width = ctx.canvas_draw.textlength(text, font = ctx.fonts.text(36))
    text_x = pos[0] + (character_img_width - text_width)//2
    text_y = pos[1] + character_img_height + 10
    draw_text(ctx.canvas_draw, (text_x, text_y), text = text, font = ctx.fonts.text(36), fill = (210, 210, 210))
    return text_x, text_y

def paste_element_img(ctx: RenderContext, character: CharacterContext, text_x, text_y):
    element_file = ctx.img_path / "element" / f"{ctx.stats_name_map[character.template[character.zh_name]['element']]}.png"
    img = Image.open(element_file)
    paste_icon(ctx.canvas, img, (int(text_x - img.width), text_y))