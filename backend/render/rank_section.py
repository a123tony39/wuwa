from PIL import Image, ImageFont
from domain.score.score import get_rank
from .canvas import paste_icon, draw_text

def paste_rank(total_score, under_panel_x, under_panel_y, canvas, canvas_draw, img_path):
    rank = get_rank(total_score)
    # rank pic
    slot_x, slot_y = under_panel_x + 51 + 85, under_panel_y + 33 + 120
    slow_w, slot_h = 180, 180
    print(f"{rank}: {total_score}")
    rank_img = load_rank_pic(rank, img_path)
    img_w, img_h = rank_img.size
    mid_x = slot_x + (slow_w - img_w) // 2
    mid_y = slot_y + (slot_h - img_h) // 2
    paste_icon(canvas, rank_img, (mid_x, mid_y))
    # set text and font
    text_zh = f"練度評分:{total_score:.2f}".rstrip('0').rstrip('.')
    font_zh = ImageFont.truetype("../ttf/NotoSansTC-Bold.ttf", 36)
    # compute and align center
    w_zh = canvas_draw.textlength(text_zh, font=font_zh)
    rank_img_center = mid_x + rank_img.width//2
    x = rank_img_center - w_zh//2
    y = mid_y + rank_img.height + 10
    draw_text(canvas_draw, (x, y), text_zh, font=font_zh, fill=(220, 220, 220))


def load_rank_pic(rank, img_path):
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
