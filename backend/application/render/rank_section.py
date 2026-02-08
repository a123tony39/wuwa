from PIL import Image
from pathlib import Path
from dataclasses import dataclass
from .context import RenderContext
from .core.canvas import paste_icon, draw_text

@dataclass
class RankLayout:
    slot_origin: tuple
    slot_size: tuple
    font_size: int
    text_color: tuple

def paste_rank(total_score: float, rank: str, ctx: RenderContext, layout: RankLayout):
    # rank img
    print(f"{rank}: {total_score}")
    rank_img = load_rank_pic(rank, ctx.img_path)
    img_paste_pos = cal_img_centered_paste_pos(rank_img, layout.slot_origin, layout.slot_size)
    paste_icon(ctx.canvas, rank_img, img_paste_pos)
    # set text and font
    text_zh = f"練度評分: {total_score:.2f}".rstrip('0').rstrip('.')
    font_zh = ctx.fonts.text(layout.font_size)
    # compute and align center
    text_paste_pos = cal_text_centered_paste_pos(ctx, text_zh, font_zh, img_paste_pos, rank_img.size)
    draw_text(ctx.canvas_draw, text_paste_pos, text_zh, font=font_zh, fill=layout.text_color)
    return rank

def load_rank_pic(rank: str, img_path: Path):
    ss_score_file = img_path / "score/SS_score.png"
    s_score_file = img_path / "score/S_score.png"
    a_score_file = img_path / "score/A_score.png"
    b_score_file = img_path / "score/B_score.png"
    f_score_file = img_path / "score/F_score.png"
    rank_images = {
        "SS": ss_score_file,
        "S": s_score_file,
        "A": a_score_file,
        "B": b_score_file,
        "F": f_score_file,
    }

    if rank in rank_images:
        return Image.open(rank_images[rank])
    else:
        raise ValueError(f"{rank} is not valid ranking")
    
def cal_img_centered_paste_pos(img, slot_pos, slot_size):
    slot_x, slot_y = slot_pos
    slot_w, slot_h = slot_size
    img_w, img_h = img.size
    paste_x = slot_x + (slot_w - img_w) // 2
    paste_y = slot_y + (slot_h - img_h) // 2
    return (paste_x, paste_y)

def cal_text_centered_paste_pos(ctx, text_zh, font_zh, img_paste_pos, img_size):
    w_zh = ctx.canvas_draw.textlength(text_zh, font=font_zh)
    rank_img_center = img_paste_pos[0] + img_size[0]//2
    x = rank_img_center - w_zh//2
    y = img_paste_pos[1] + img_size[1] + 10
    return (x, y)