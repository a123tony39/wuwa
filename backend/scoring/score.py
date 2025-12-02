import yaml

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

def calculate_score(stat_name, stat_value, BASE_SCORE, STATS_EXPECT_BIAS):
    base = BASE_SCORE.get(stat_name)
    info = STATS_EXPECT_BIAS.get(stat_name)
    min, max = info['min'], info['max']
    bias, expect = info['bias'], info['expect']

    score = round(base + bias + (stat_value - expect) / (max - min), 2)
    return score

def get_score(echo, character_name):
    BASE_SCORE = load_yaml("./scoring/base_score.yaml")
    STAT_CATEGORIES = load_yaml("./scoring/stats_categories.yaml")
    CHARACTER_TEMPLATE = load_yaml("./scoring/character_template.yaml")
    STATS_EXPECT_BIAS = load_yaml("./scoring/stats_expect_bias.yaml") 
    valid = get_valid_stats(character_name, STAT_CATEGORIES, CHARACTER_TEMPLATE)

    total_score = 0
    print("--------聲骸評分--------")
    print(f"角色: {character_name} 適用詞條: {valid}")
    for stat in echo.sub_stat:
        if stat.name not in valid:
            continue
        
        echo_score = calculate_score(stat.name, stat.value, BASE_SCORE, STATS_EXPECT_BIAS) * 4
        total_score += echo_score
        print(f"{stat.name} : {stat.value} : {echo_score}")

    print(f"Total : {total_score}")
    return total_score

def compute_stat_expect(data):
    result = {}
    for stat, tiers in data.items():
        expect = 0
        # print(stat, info)
        global_min = None
        global_max = None
        for _, info in tiers.items():
            min, max = info['range']
            total_rate = info['rate'] * info['cnt']
            expect += ((min+max)/2) * (total_rate/100)
        
            if global_min is None:
                global_min = min
            global_max = max
        expect = round(expect, 2)
        bias = round(-(global_min-expect) / (global_max - global_min), 2) 
       
        result[stat] = {'min': global_min, 'max': global_max, 'bias': bias, 'expect': expect}
    return result
    
def get_stat_tier(stat_name, value, config):
    tiers = config.get(stat_name)
    if not tiers:
        return None

    for tier, info in tiers.items():
        low, high = info['range']
        if low <= value <= high:
            return tier
    
    return None

def get_rank(score):
    if score >= 90:
        return "SS"
    elif score >= 80:
        return "S"
    elif score >= 60:
        return "A"
    else:
        return "B"
    

if __name__ == "__main__":
    STATS_TIER_RANGE = load_yaml("./stats_tier_range.yaml")
    STATS_EXPECT_BIAS = load_yaml("./stats_expect_bias.yaml") 
    result = compute_stat_expect(STATS_TIER_RANGE)
    print(result)
    with open("stats_expect_bias.yaml", "w", encoding="utf-8") as f:
        yaml.dump(result, f, allow_unicode=True)

    # score = calculate_score("暴擊", 6.3, STATS_EXPECT_BIAS)
    # print(score)
    # score = calculate_score("暴擊", 7.5, STATS_EXPECT_BIAS)
    # print(score)
    # score = calculate_score("暴擊", 10.5, STATS_EXPECT_BIAS)
    # print(score)

    # score = calculate_score("生命", 580, STATS_EXPECT_BIAS)
    # print(score)

    # score = calculate_score("生命", 441, STATS_EXPECT_BIAS)
    # print(score)

    score = calculate_score("暴擊傷害", 15.0, STATS_EXPECT_BIAS)
    print(score)

    score = calculate_score("攻擊", 60, STATS_EXPECT_BIAS)
    print(score)
