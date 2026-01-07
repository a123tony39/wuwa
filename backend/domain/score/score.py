from domain.stats.cal_cdf import compute_discrete_cdf

ECHO_SCORE_LEVELS = {
    "PERFECT": 15,
    "GOOD": 10,
}

def calculate_stat_score(stat_name, stat_value, base_score, stats_tier_range):
    max_contribution = base_score.get(stat_name)
    info = stats_tier_range.get(stat_name)
    quality_ratio = compute_discrete_cdf(stat_table = info, value = stat_value)
    score = max_contribution * (0.7 + 0.3 * quality_ratio)
    return score

def get_score(echo, valid_stats, character_name, base_score, stats_tier_range):
    print("採用base_score:", base_score)
    breakdown = []
    echo_score = 0
    print(f"角色: {character_name} 適用詞條: {valid_stats}")
    for stat in echo.sub_stat:
        if stat.name not in valid_stats:
            breakdown.append((stat.name, stat.value, 0))
            continue
        
        stat_score = calculate_stat_score(stat.name, stat.value, base_score, stats_tier_range)
        echo_score += stat_score
        breakdown.append((stat.name, stat.value, stat_score))
        print(f"{stat.name} : {stat.value} : {stat_score}")

    score_ceiling = base_score["分數上限"]
    echo_completion = (echo_score / score_ceiling) * 20
    return echo_completion, breakdown

def get_rank(score):
    if score >= 80:
        return "SS"
    elif score >= 70:
        return "S"
    elif score >= 60:
        return "A"
    elif score >= 50:
        return "B"
    else:
        return "F"