import difflib
def get_character_zh_and_en_name(character_name, character_template):
    if character_name in character_template:
        return [character_name, character_template[character_name]['en']]

    candidates = list(character_template.keys())
    close = difflib.get_close_matches(character_name, candidates, n=1, cutoff=0.3)
    if close:
        best_match = close[0]
        return [best_match, character_template[best_match]['en']]
    
    raise ValueError(f"Unknown character name: {character_name}")

def get_valid_stats_and_role(character_name, stats_categories, character_templates):
    template = character_templates[character_name]
    valid = set()
    # main_attr
    valid.update(stats_categories["main_attr"][template["main_attr"]])
    # dmg_type
    for dmg in template["dmg_type"]:
        valid.update(stats_categories["dmg_type"][dmg])
    # role
    role = template["role"]
    valid.update(stats_categories["role"][role])
    # element
    valid.update(stats_categories["element"][template["element"]])
    return valid, role