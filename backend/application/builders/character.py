from pathlib import Path
from infrastructure.yaml_io import load_yaml

from domain.score.rules import ScoreRules
from domain.character.get_character_info import get_character_zh_and_en_name, get_valid_stats, get_base_score
from domain.character.context import CharacterContext
from domain.player.player_info import get_player_info
from domain.player.context import PlayerInfo

def build_character_context(ocr_results) -> tuple[CharacterContext, ScoreRules, PlayerInfo]:
    score_rules = load_score_rules()
    character_template = load_character_template()
    player_info = get_player_info(ocr_results.player_block)
    character_zh_name, character_en_name = get_character_zh_and_en_name(
        character_name = player_info.character_name, 
        character_template = character_template
    )
    valid_stats = get_valid_stats(character_zh_name, score_rules.stats_categories, character_template)
    base_score = get_base_score(character_zh_name, character_template, score_rules.base_score)
    character_ctx = CharacterContext(
        zh_name = character_zh_name,
        en_name = character_en_name,
        template = character_template,
        valid_stats = valid_stats,
        base_score = base_score,
    )

    return character_ctx, score_rules, player_info

def load_score_rules(domain_path: Path = Path("./domain")) -> ScoreRules:
    base_score = load_yaml(domain_path / "score" / "base_score.yaml")
    stats_name_map = load_yaml(domain_path / "stats" / "stats_name_map.yaml")
    stats_categories = load_yaml(domain_path / "stats" / "stats_categories.yaml")
    stats_tier_range = load_yaml(domain_path / "stats" / "stats_tier_range.yaml") 
    return ScoreRules(base_score, stats_name_map, stats_categories, stats_tier_range)

def load_character_template(path = Path("./domain/character/character_template.yaml")):
    return load_yaml(path)