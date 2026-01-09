import pytest
from domain.score.score import get_score
from domain.echo.ocr_parser import EchoData, Stat
from infrastructure.yaml_io import load_yaml

def create_fake_echo():
    echo = load_yaml("./tests/test_fixtures/echo.yaml")
    fake_echo = EchoData()
    fake_echo.main_stat = Stat(**echo["main_stat"])
    fake_echo.static_stat = Stat(**echo["static_stat"])
    fake_echo.sub_stat = [Stat(**s) for s in echo["sub_stat"]]
    return fake_echo

def test_empty_get_score():
    echo = EchoData(sub_stat=[])
    
    valid_stats = {"攻擊", "生命"}
    character_name = "角色A"

    total_score, breakdown = get_score(echo, valid_stats, character_name, {"分數上限": 1}, {})
    
    assert total_score == 0
    assert breakdown == []

def test_get_score():
    character = "弗洛洛"
    fake_echo = create_fake_echo()
    base_score = load_yaml("./domain/score/base_score.yaml")
    stats_tier_range = load_yaml("./domain/stats/stats_tier_range.yaml") 
    total_score, breakdown = get_score(
        fake_echo, 
        {"暴擊", "暴擊傷害", "攻擊", "攻擊%", "湮滅傷害加成", "共鳴技能傷害加成"}, 
        character, 
        base_score["輸出"], 
        stats_tier_range
    )

    assert total_score == pytest.approx(14.02368) 
    names = [s[0] for s in breakdown]
    assert names == ["暴擊", "防禦%", "攻擊%", "暴擊傷害", "攻擊"]
    score_map = {name: score for name, _, score in breakdown}
    assert score_map["攻擊"] == pytest.approx(0.856)
    assert score_map["攻擊%"] == pytest.approx(3.208)
    assert score_map["暴擊"] == pytest.approx(7.2992)
    assert score_map["暴擊傷害"] == pytest.approx(6.166399999999999)

    # assert breakdown == [('暴擊', 7.5, 7.2992), ('防禦%', 8.1, 0), ('攻擊%', 7.9, 3.2079999999999997), ('暴擊傷害', 12.6, 6.166399999999999), ('攻擊', 40.0, 0.856)]

if __name__ == "__main__":
    test_get_score()