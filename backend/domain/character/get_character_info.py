import difflib
from pathlib import Path
from backend.infrastructure.yaml_io import load_yaml

def get_character_zh_and_en_name(character_name, character_template):
    if character_name in character_template:
        return [character_name, character_template[character_name]['en']]

    candidates = list(character_template.keys())
    close = difflib.get_close_matches(character_name, candidates, n=1, cutoff=0.3)
    if close:
        best_match = close[0]
        return [best_match, character_template[best_match]['en']]
    
    raise ValueError(f"Unknown character name: {character_name}")

def get_valid_stats(character_name, stats_categories, character_templates):
    template = character_templates[character_name]
    valid = set()
    # main_attr
    valid.update(stats_categories["main_attr"][template["main_attr"]])
    # dmg_type
    for dmg in template["dmg_type"]:
        valid.update(stats_categories["dmg_type"][dmg])
    # stat_rule
    valid_stat_rule = template["valid_stat_rule"]
    valid.update(stats_categories["valid_stat"][valid_stat_rule])
    # element
    valid.update(stats_categories["element"][template["element"]])
    return valid

def get_base_score(character_name, character_templates, score_template):
    base_score_rule = character_templates[character_name]['base_score_rule']
    return score_template[base_score_rule]

def load_character_template(path = Path("backend/domain/character/character_template.yaml")):
    return load_yaml(path)