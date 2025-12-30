class ScoreRules:
    def __init__(
        self,
        base_score: dict,
        stats_name_map: dict,
        stats_categories: dict,
        stats_expects_bias: dict,
    ):
        self.base_score = base_score
        self.stats_name_map = stats_name_map
        self.stats_categories = stats_categories
        self.stats_expects_bias = stats_expects_bias
    
    def get_role_base_score(self, role: str):
        return self.base_score[role]