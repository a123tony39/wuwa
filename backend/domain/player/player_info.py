from .context import PlayerInfo

def get_player_info(info):
    character_name, player_name, uid = None, None, None
    for text in info:
        if character_name is None:
            character_name = text
        elif "玩家名稱" in text:
            colon_pos = text.find(":")
            if colon_pos != -1:
                player_name = text[colon_pos+1:].strip()
        elif "特徵碼" in text:
            colon_pos = text.find(":")
            if colon_pos != -1:
                uid = text[colon_pos+1:].strip()

    return PlayerInfo(
        player_name = player_name, 
        character_name = character_name, 
        uid = uid,
    )