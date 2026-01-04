from infrastructure.yaml_io import load_yaml, write_yaml

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

if __name__ == "__main__":
    STATS_TIER_RANGE = load_yaml("./stats_tier_range.yaml")
    STATS_EXPECT_BIAS = load_yaml("./stats_expect_bias.yaml") 
    result = compute_stat_expect(STATS_TIER_RANGE)
    print(result)
    write_yaml("stats_expect_bias.yaml", result)