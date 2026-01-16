from render.echo_section import EchoLayout, main_stat_frame_size
from render.top_right_section import TopRightLayout, stat_frame_size

# === base positions ===
CHARACTER_IMG_POSITION = (80, 119)
UNDER_PANEL_POSITION = (145, 1079)

# === top right section ===
TOP_RIGHT_LAYOUT = TopRightLayout(
    origin_x = 737,
    origin_y = CHARACTER_IMG_POSITION[1] + 50,
    stat_frame_size = stat_frame_size(500, 70),
    text_right_padding = 10,
    line_gap = 17.5
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
    stat_positions=[
        (UNDER_PANEL_POSITION[0] + ECHO_FRAME_WIDTH, UNDER_PANEL_POSITION[1]), 
        (UNDER_PANEL_POSITION[0] + ECHO_FRAME_WIDTH * 2, UNDER_PANEL_POSITION[1]), 
        (UNDER_PANEL_POSITION[0], UNDER_PANEL_POSITION[1] + ECHO_FRAME_HEIGHT),
        (UNDER_PANEL_POSITION[0] + ECHO_FRAME_WIDTH, UNDER_PANEL_POSITION[1] + ECHO_FRAME_HEIGHT),
        (UNDER_PANEL_POSITION[0] + ECHO_FRAME_WIDTH * 2, UNDER_PANEL_POSITION[1] + ECHO_FRAME_HEIGHT),
    ],
    main_stat_frame_size = main_stat_frame_size(230, 50),
    sub_stat_width = 330
)