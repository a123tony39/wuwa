from domain.character.get_character_info import get_valid_stats, get_base_score
from infrastructure.yaml_io import load_yaml

base_score_templates = load_yaml("./domain/score/base_score.yaml")
stats_categories = load_yaml("./domain/stats/stats_categories.yaml")
character_templates = load_yaml("./domain/character/character_template.yaml")
def test_phorlova():
    valid = get_valid_stats(
        character_name = "弗洛洛", 
        character_templates = character_templates,
        stats_categories = stats_categories
    )

    assert valid == {"攻擊", "攻擊%", "共鳴技能傷害加成", "暴擊", "暴擊傷害", "湮滅傷害加成"}

def test_brant_base_score():
    base_score = get_base_score(
        character_name = "布蘭特", 
        character_templates = character_templates,
        score_template = base_score_templates,
    )

    assert base_score == {"共鳴效率": 8, "暴擊": 6, "暴擊傷害": 6, "攻擊%": 4, "普攻傷害加成": 4, "攻擊": 1}

def test_multiple_dmg_type():
    valid = get_valid_stats(
        character_name = "卡提希婭", 
        character_templates = character_templates,
        stats_categories = stats_categories
    )

    assert valid == {"生命", "生命%", "普攻傷害加成", "共鳴解放傷害加成", "暴擊", "暴擊傷害", "共鳴效率", "氣動傷害加成"}