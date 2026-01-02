import pytest
from domain.score.score import get_score
from domain.echo.ocr_parser import EchoData, Stat
from infrastructure.yaml_config.yaml import load_yaml

def test_empty_get_score():
    echo = EchoData(sub_stat=[])
    
    valid_stats = {"攻擊", "生命"}
    character_name = "角色A"

    total_score, breakdown = get_score(echo, valid_stats, character_name, {}, {})
    
    assert total_score == 0
    assert breakdown == []
