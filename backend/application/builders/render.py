
from collections import defaultdict

from domain.score.score import get_rank
from domain.stats.rules import stat_sort_key, normalize_stats, merge_flat_and_percent_stats, FLAT_STATS

from render.context import build_render_context
from render.top_left_section import render_top_left_section
from render.echo_section import render_echo_section
from render.top_right_section import render_top_right_section
from render.rank_section import paste_rank
from config.layout import ECHO_LAYOUT, CHARACTER_IMG_POSITION, TOP_RIGHT_LAYOUT, UNDER_PANEL_POSITION

class RenderAgent:
    def __init__(self, character_ctx, score_rules, source, background_image):
        self.character_ctx = character_ctx
        self.score_rules = score_rules
        self.source = source
        self.background_image = background_image
        self.render_ctx = build_render_context(self.character_ctx, self.score_rules, self.background_image)

    def render_top_left(self, player_info):
        render_top_left_section(
            ctx = self.render_ctx,
            character = self.character_ctx,
            player_info = player_info,
            character_img_position = CHARACTER_IMG_POSITION,
        )

    def render_echo(self, ocr_results):
        self.total_stats = defaultdict(float)
        self.total_score, self.echo_results = render_echo_section(
            ctx = self.render_ctx,
            character = self.character_ctx,
            layout = ECHO_LAYOUT,
            rules = self.score_rules,
            source = self.source,
            total_stats = self.total_stats,
            ocr_results = ocr_results.echo_block,
        )

    def render_top_right(self):
        self.total_stats = merge_flat_and_percent_stats(self.total_stats, FLAT_STATS)
        allowed_stats = normalize_stats(self.character_ctx.valid_stats, FLAT_STATS) | FLAT_STATS
        sorted_allowed_stats = sorted(allowed_stats, key = lambda x : stat_sort_key(x))

        render_top_right_section(
            ctx = self.render_ctx,
            FLAT_STATS = FLAT_STATS,
            total_stats = self.total_stats, 
            layout = TOP_RIGHT_LAYOUT,
            sorted_allowed_stats = sorted_allowed_stats,
        )

    def render_rank(self):
        self.rank = get_rank(self.total_score)
        paste_rank(
            ctx = self.render_ctx,
            rank = self.rank, 
            total_score = self.total_score,
            panel_position = UNDER_PANEL_POSITION,
        )
    
    def get_canvas(self):
        return self.render_ctx.canvas