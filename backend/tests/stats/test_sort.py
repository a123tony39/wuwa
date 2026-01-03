from domain.stats.rules import stat_sort_key, merge_flat_and_percent_stats, FLAT_STATS

def test_stat_sort_key_priority_first():
    base_stats = ["生命", "攻擊", "防禦"]
    crit_stats = ["暴擊", "暴擊傷害"]

    for base in base_stats:
        for crit in crit_stats:
            assert stat_sort_key(base) < stat_sort_key(crit)

def test_stat_sort_key_unknown_sorted_by_length():
    assert stat_sort_key("湮滅傷害加成") < stat_sort_key("共鳴解放傷害加成")


def test_merge_flat_and_percent_stats():
    total_stats = {
        "攻擊": 150,
        "攻擊%": 11.6,
        "生命": 180,
        "生命%": 5,
        "防禦": 120,
        "防禦%": 10,
        "暴擊": 9,
        "暴擊傷害": 10.5
    }
    merged = merge_flat_and_percent_stats(total_stats, FLAT_STATS)
    assert merged["攻擊"] == [150, 11.6]
    assert merged["生命"] == [180, 5]
    assert merged["防禦"] == [120, 10]

    assert merged["暴擊"] == 9
    assert merged["暴擊傷害"] == 10.5

    assert "攻擊%" not in merged
    assert "生命%" not in merged
    assert "防禦%" not in merged