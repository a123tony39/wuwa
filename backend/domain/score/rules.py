from pathlib import Path
from infrastructure.yaml_io import load_yaml

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

def load_score_rules(domain_path: Path = Path("./domain")) -> ScoreRules:
    base_score = load_yaml(domain_path / "score" / "base_score.yaml")
    stats_name_map = load_yaml(domain_path / "stats" / "stats_name_map.yaml")
    stats_categories = load_yaml(domain_path / "stats" / "stats_categories.yaml")
    stats_tier_range = load_yaml(domain_path / "stats" / "stats_tier_range.yaml") 
    return ScoreRules(base_score, stats_name_map, stats_categories, stats_tier_range)