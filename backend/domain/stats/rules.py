STAT_GROUP_PRIORITY = {
    "生命": (0, 0),  
    "攻擊": (0, 1),
    "防禦": (0, 2),
    "共鳴效率": (1, 0),
    "暴擊": (2, 0),
    "暴擊傷害": (2, 1),
}
FLAT_STATS = {"生命", "攻擊", "防禦"}

def stat_sort_key(stat_name: str):
    if stat_name in STAT_GROUP_PRIORITY:
        return (*STAT_GROUP_PRIORITY[stat_name], 0)
    return (99, 0, len(stat_name))

def normalize_stats(valid_stats, flat_stats):
    flat_percent = {f"{s}%" for s in flat_stats}
    return valid_stats - flat_percent


def merge_flat_and_percent_stats(total_stats, FLAT_STATS):
    merged = dict(total_stats)  
    for base_stat in FLAT_STATS:
        flat_val = merged.get(base_stat, 0)
        percent_val = merged.get(f"{base_stat}%", 0)
        merged[base_stat] = [flat_val, percent_val]
        merged.pop(f"{base_stat}%", None)
    return merged