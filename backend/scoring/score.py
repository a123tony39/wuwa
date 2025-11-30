import yaml

def load_yaml(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_valid_stats(character_name, stat_categories, character_templates):
    template = character_templates[character_name]
    valid = set()
    # main_attr
    valid.update(stat_categories["main_attr"][template["main_attr"]])
    # dmg_type
    valid.update(stat_categories["dmg_type"][template["dmg_type"]])
    # role
    valid.update(stat_categories["role"][template["role"]])
    return valid
STAT_CATEGORIES = load_yaml("stats_categories.yaml")
CHARACTER_TEMPLATE = load_yaml("character_template.yaml")
print(get_valid_stats("贊尼", STAT_CATEGORIES, CHARACTER_TEMPLATE))
stats_range = {
    "生命": (320, 580),
    "生命%": (6.4, 11.6),
    "攻擊": (30, 60),
    "攻擊%": (6.4, 11.6),
    "防禦": (40, 60),
    "防禦%": (8.1, 15),
    "暴擊" : (6.3, 10.5),
    "暴擊傷害" : (12.6, 21),
    "普攻傷害加成": (6.4, 11.6),
    "重擊傷害加成": (6.4, 11.6),
    "共鳴技能傷害加成": (6.4, 11.6),
    "共鳴解放傷害加成": (6.4, 11.6),
    "共鳴效率": (6.8, 12.4),
}
PERCENTABLE = ["生命", "攻擊", "防禦"]
def calculate_score(echo):
    score = 0
    for sub in echo.sub_stat:
        if sub.type in PERCENTABLE:
            key = f"{sub.type}%" if "%" in sub.type else sub.type
        else:
            key = sub.type
        max = stats_range[key][1]
        score += (float(sub.value.replace("%", "")) / max) * 4

    print(score)
    return score

def get_rank(score):
    if score >= 90:
        return "SS"
    elif score >= 80:
        return "S"
    elif score >= 60:
        return "A"
    else:
        return "B"