
stats_range = {
    ("生命", ""): (320, 580),
    ("生命", "%"): (6.4, 11.6),
    ("攻擊", ""): (30, 60),
    ("攻擊", "%"): (6.4, 11.6),
    ("防禦", ""): (40, 60),
    ("防禦", "%"): (8.1, 15),
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
            key = (sub.type, "%") if "%" in sub.type else (sub.type, "")
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