from PIL import Image
import numpy as np

def get_player_info(source, reader):
    cropped = source.crop((0, 0, 300, 150))

    cropped = cropped.resize(
        (int(cropped.width*2), int(cropped.height*2)),
        resample=Image.NEAREST,
    )
    cropped = cropped.convert("L")
    cropped_np = np.array(cropped)
    results = reader.readtext(cropped_np)

    character_name, player_name, uid = None, None, None
    for _, text, _ in results:
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

    return {
        "player_name": player_name, 
        "character_name": character_name, 
        "uid": uid,
    }