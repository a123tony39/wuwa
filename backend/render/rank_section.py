from PIL import Image
from pathlib import Path
from .context import RenderContext
from .core.canvas import paste_icon, draw_text

def paste_rank(total_score: float, rank: str, ctx: RenderContext, panel_position: tuple):
    # rank pic
    slot_x, slot_y = panel_position[0] + 85, panel_position[1] + 120
    slow_w, slot_h = 180, 180
    print(f"{rank}: {total_score}")
    rank_img = load_rank_pic(rank, ctx.img_path)
    img_w, img_h = rank_img.size
    mid_x = slot_x + (slow_w - img_w) // 2
    mid_y = slot_y + (slot_h - img_h) // 2
    paste_icon(ctx.canvas, rank_img, (mid_x, mid_y))
    # set text and font
    text_zh = f"練度評分: {total_score:.2f}".rstrip('0').rstrip('.')
    font_zh = ctx.fonts.text(36)
    # compute and align center
    w_zh = ctx.canvas_draw.textlength(text_zh, font=font_zh)
    rank_img_center = mid_x + rank_img.width//2
    x = rank_img_center - w_zh//2
    y = mid_y + rank_img.height + 10
    draw_text(ctx.canvas_draw, (x, y), text_zh, font=font_zh, fill=(220, 220, 220))
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