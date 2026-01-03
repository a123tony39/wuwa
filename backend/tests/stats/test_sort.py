from domain.stats.rules import stat_sort_key

def test_stat_sort_key_priority_first():
    assert stat_sort_key("生命") < stat_sort_key("暴擊")

def test_stat_sort_key_unknown_sorted_by_length():
    assert stat_sort_key("湮滅傷害加成") < stat_sort_key("共鳴解放傷害加成")