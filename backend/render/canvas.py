


def draw_text(
    canvas_draw,
    pos,
    text,
    *,
    font,
    fill,
    anchor=None,
    align=None,
    spacing=0,
    stroke_width=0,
    stroke_fill=None,
):
    canvas_draw.text(
        pos,
        text=text,
        font=font,
        fill=fill,
        anchor=anchor,
        align=align,
        spacing=spacing,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )

def paste_icon(canvas, icon, pos):
    if icon.mode == "RGBA":
        canvas.paste(icon, pos, icon)
    else:
        canvas.paste(icon, pos)