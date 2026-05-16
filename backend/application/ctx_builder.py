from ..domain.player.context import PlayerInfo
from ..domain.player.parser import get_player_info
from ..domain.character.context import CharacterContext
from ..domain.score.rules import ScoreRules, load_score_rules
from ..domain.character.get_character_info import get_character_zh_and_en_name, get_valid_stats, get_base_score, load_character_template
from dataclasses import dataclass

@dataclass
class PreparedData:
    character: CharacterContext
    score_rules: ScoreRules
    player_info: PlayerInfo

def prepare_character_analysis_context(ocr_player_block):
    score_rules, character_template = load_analysis_rules()
    player_info, zh_name, en_name = parse_player_and_character(
        ocr_player_block, character_template
    )
    character_ctx = build_character_context(
        zh_name, en_name, character_template, score_rules
    )

    return PreparedData(
        character=character_ctx,
        score_rules=score_rules,
        player_info=player_info,
    )

def load_analysis_rules():
    score_rules = load_score_rules()
    character_template = load_character_template()
    return score_rules, character_template

def parse_player_and_character(ocr_player_block, character_template):
    player_info = get_player_info(ocr_player_block)

    zh_name, en_name = get_character_zh_and_en_name(
        character_name=player_info.character_name,
        character_template=character_template
    )
    return player_info, zh_name, en_name

def build_character_context(
    zh_name,
    en_name,
    character_template,
    score_rules,
):
    valid_stats = get_valid_stats(
        character_name = zh_name,
        character_templates = character_template,
        stats_categories = score_rules.stats_categories

    )
    base_score = get_base_score(
        character_name = zh_name,
        character_templates = character_template,
        score_template = score_rules.base_score
    )

    return CharacterContext(
        zh_name=zh_name,
        en_name=en_name,
        template=character_template,
        valid_stats=valid_stats,
        base_score=base_score,
    )



