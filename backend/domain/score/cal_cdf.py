def expand_stat_table(stat_table: dict) -> list[tuple[float, float]]:
    """
    return [(value, probability), ...]
    """
    result = []

    for tier in stat_table.values():
        low, high = tier["range"]
        cnt = tier["cnt"]
        rate = round(tier["rate"] / 100.0, 4)
        
        if cnt == 1:
            values = [low]
        else:
            step = (high-low) / (cnt-1)
            values = [low + i * step for i in range(cnt)]
        
        for v in values:
            result.append((v, rate))
    
    return result

def compute_discrete_cdf(stat_table: dict, value: float):
    pairs = expand_stat_table(stat_table)
    cdf = sum(prob for v, prob in pairs if v <= value)

    return min(cdf, 1.0)