from domain.score.score import get_rank
from domain.stats.rules import stat_sort_key, filter_flat_percent_stats, FLAT_STATS, merge_flat_and_percent_stats

from render.context import build_render_context
from render.top_left_section import render_top_left_section
from render.echo_section import render_echo_section
from render.top_right_section import render_top_right_section
from render.rank_section import paste_rank
from config.layout import ECHO_LAYOUT, CHARACTER_IMG_POSITION, TOP_RIGHT_LAYOUT, RANKLAYOUT

class RenderAgent:
    def __init__(self, character_ctx,  character_summary, score_rules, background_image):
        self.character_ctx = character_ctx
        self.character_summary = character_summary
        self.score_rules = score_rules
        self.background_image = background_image
        self.render_ctx = build_render_context(self.character_ctx, self.score_rules, self.background_image)

    def render_top_left(self, player_info):
        render_top_left_section(
            character_img_position = CHARACTER_IMG_POSITION,
            ctx = self.render_ctx,
            character = self.character_ctx,
            player_info = player_info,
        )

    def render_echo(self, source):
        render_echo_section(
            layout = ECHO_LAYOUT,
            source = source,
            ctx = self.render_ctx,
            character = self.character_ctx,
            character_summary = self.character_summary,
        )

    def render_top_right(self):
        sorted_allowed_stats = prepare_top_right_stats(self.character_ctx, FLAT_STATS)
        stats_total_value = merge_flat_and_percent_stats(self.character_summary.stats_total_value, FLAT_STATS)
        render_top_right_section(
            layout = TOP_RIGHT_LAYOUT,
            ctx = self.render_ctx,
            FLAT_STATS = FLAT_STATS,
            sorted_allowed_stats = sorted_allowed_stats,
            stats_total_value = stats_total_value, 
        )

    def render_rank(self):
        self.rank = get_rank(self.character_summary.total_score)
        paste_rank(
            ctx = self.render_ctx,
            rank = self.rank, 
            layout = RANKLAYOUT,
            total_score = self.character_summary.total_score,
        )
    
    def get_canvas(self):
        return self.render_ctx.canvas
    
def prepare_top_right_stats(character_ctx, FLAT_STATS):
    no_flat_percent_stats = filter_flat_percent_stats(character_ctx.valid_stats, FLAT_STATS) | FLAT_STATS
    return sorted(no_flat_percent_stats, key = lambda x : stat_sort_key(x))