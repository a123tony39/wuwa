from render.echo_section import EchoLayout
from render.top_right_section import TopRightLayout

# === base positions ===
CHARACTER_IMG_POSITION = (80, 119)
UNDER_PANEL_POSITION = (145, 1079)

# === top right section ===
TOP_RIGHT_LAYOUT = TopRightLayout(
    origin_x = 737,
    origin_y = CHARACTER_IMG_POSITION[1] + 50,
)

# === echo section ===
ECHO_FRAME_WIDTH = 350
ECHO_FRAME_HEIGHT = 420

ECHO_LAYOUT = EchoLayout(
    avatar_positions=[
        (0, 650),
        (380, 650),
        (760, 650),
        (1140, 650),
        (1520, 650),
    ],
    paste_positions=[
        (UNDER_PANEL_POSITION[0] + ECHO_FRAME_WIDTH, UNDER_PANEL_POSITION[1]), 
        (UNDER_PANEL_POSITION[0] + ECHO_FRAME_WIDTH * 2, UNDER_PANEL_POSITION[1]), 
        (UNDER_PANEL_POSITION[0], UNDER_PANEL_POSITION[1] + ECHO_FRAME_HEIGHT),
        (UNDER_PANEL_POSITION[0] + ECHO_FRAME_WIDTH, UNDER_PANEL_POSITION[1] + ECHO_FRAME_HEIGHT),
        (UNDER_PANEL_POSITION[0] + ECHO_FRAME_WIDTH * 2, UNDER_PANEL_POSITION[1] + ECHO_FRAME_HEIGHT),
    ],
)