from domain.player.context import get_player_info

def test_get_player_info_normal():
    info = ["卡提希婭", "玩家名稱:Testuseer01", "特徵碼:80006666"]
    result = get_player_info(info)
    assert result.character_name == "卡提希婭"
    assert result.player_name == "Testuseer01"
    assert result.uid == "80006666"

def test_missing_fields():
    info = ["角色B", "特徵碼:6789"]
    result = get_player_info(info)
    assert result.character_name == "角色B"
    assert result.player_name is None
    assert result.uid == "6789"

def test_empty_list():
    info = []
    result = get_player_info(info)
    assert result.character_name is None
    assert result.player_name is None
    assert result.uid is None
