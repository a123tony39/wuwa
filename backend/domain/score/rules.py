class ScoreRules:
    def __init__(
        self,
        base_score: dict,
        stats_name_map: dict,
        stats_categories: dict,
        stats_tier_range: dict,
    ):
        self.base_score = base_score
        self.stats_name_map = stats_name_map
        self.stats_categories = stats_categories
        self.stats_tier_range = stats_tier_range