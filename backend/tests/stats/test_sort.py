from domain.stats.rules import stat_sort_key

def test_stat_sort_key_priority_first():
    base_stats = ["生命", "攻擊", "防禦"]
    crit_stats = ["暴擊", "暴擊傷害"]

    for base in base_stats:
        for crit in crit_stats:
            assert stat_sort_key(base) < stat_sort_key(crit)

def test_stat_sort_key_unknown_sorted_by_length():
    assert stat_sort_key("湮滅傷害加成") < stat_sort_key("共鳴解放傷害加成")