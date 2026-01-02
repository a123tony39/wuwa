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

def calculate_score(stat_name, stat_value, BASE_SCORE, STATS_EXPECT_BIAS):
    base = BASE_SCORE.get(stat_name)
    info = STATS_EXPECT_BIAS.get(stat_name)
    min, max = info['min'], info['max']
    bias, expect = info['bias'], info['expect']
    quality_ratio = bias + (stat_value - expect) / (max - min)
    score = base * (0.7 + 0.3 * quality_ratio)
    return score

def get_score(echo, valid_stats, character_name, base_score, stats_expects_bias):
    print("採用base_score:", base_score)
    breakdown = []
    total_score = 0
    print(f"角色: {character_name} 適用詞條: {valid_stats}")
    for stat in echo.sub_stat:
        if stat.name not in valid_stats:
            breakdown.append((stat.name, stat.value, 0))
            continue
        
        echo_score = calculate_score(stat.name, stat.value, base_score, stats_expects_bias)
        total_score += echo_score
        breakdown.append((stat.name, stat.value, echo_score))
        print(f"{stat.name} : {stat.value} : {echo_score}")

    print(f"Total : {total_score}")
    if total_score <= 13:
        print("建議加強此聲骸")
    return total_score, breakdown

    
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
    if score >= 95:
        return "SS"
    elif score >= 85:
        return "S"
    elif score >= 75:
        return "A"
    elif score >= 60:
        return "B"
    else:
        return "F"