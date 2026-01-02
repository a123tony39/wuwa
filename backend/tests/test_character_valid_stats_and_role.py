from domain.character.get_character_info import get_valid_stats_and_role
stat_categories = {
    "main_attr": {
        "生命": [
            "生命%",
            "生命"
        ],
        "攻擊": [
            "攻擊%",
            "攻擊"
        ]
    },
    "dmg_type": {
        "普攻": [
            "普攻傷害加成"
        ],
        "重擊": [
            "重擊傷害加成"
        ],
        "共鳴技能": [
            "共鳴技能傷害加成"
        ],
        "共鳴解放": [
            "共鳴解放傷害加成"
        ]
    },
    "role": {
        "弗洛洛": [
            "暴擊",
            "暴擊傷害"
        ],
        "輸出": [
            "暴擊",
            "暴擊傷害",
            "共鳴效率"
        ],
        "輔助": [
            "生命",
            "生命%",
            "治療效果加成",
            "共鳴效率"
        ]
    },
    "element": {
        "氣動": [
            "氣動傷害加成"
        ],
        "湮滅": [
            "湮滅傷害加成"
        ],
        "衍射": [
            "衍射傷害加成"
        ],
        "熱熔": [
            "熱熔傷害加成"
        ],
        "冷凝": [
            "冷凝傷害加成"
        ],
        "導電": [
            "導電傷害加成"
        ]
    }
}


def test_phorlova():
    character_templates = {
        "弗洛洛": {
            "en": "Phrolova",
            "main_attr": "攻擊",
            "dmg_type": [
                "共鳴技能"
            ],
            "role": "弗洛洛",
            "element": "湮滅"
        }
    }
    valid, role = get_valid_stats_and_role(
        character_name = "弗洛洛", 
        character_templates = character_templates,
        stat_categories = stat_categories
    )

    assert valid == {"攻擊", "攻擊%", "共鳴技能傷害加成", "暴擊", "暴擊傷害", "湮滅傷害加成"}
    assert role == "弗洛洛"


def test_multiple_dmg_type():
    character_templates = {
        "卡提希婭": {
            "en": "Cartethyia",
            "main_attr": "生命",
            "dmg_type": ["普攻", "共鳴解放"],
            "role": "輸出",
            "element": "氣動"
        }
    }
    valid, role = get_valid_stats_and_role(
        character_name = "卡提希婭", 
        character_templates = character_templates,
        stat_categories = stat_categories
    )

    assert valid == {"生命", "生命%", "普攻傷害加成", "共鳴解放傷害加成", "暴擊", "暴擊傷害", "共鳴效率", "氣動傷害加成"}
    assert role == "輸出"