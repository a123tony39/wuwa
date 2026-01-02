import pytest
from domain.character.get_character_info import get_character_zh_and_en_name

def test_exact_match():
    template = {
        "千咲": {"en": "Chisa"},
    }
    zh, en = get_character_zh_and_en_name("千咲", template)
    assert zh == "千咲"
    assert en == "Chisa"

@pytest.mark.parametrize(
    "input_name,expected_zh,expected_en",
    [
        ("千关", "千咲", "Chisa"),
        ("千", "千咲", "Chisa"), 
    ]
)
def test_fuzzy_match(input_name, expected_zh, expected_en):
    template = {
        "千咲": {"en": "Chisa"},
    }
    zh, en = get_character_zh_and_en_name(input_name, template)
    assert zh == expected_zh
    assert en == expected_en

def test_unknown_character_raises():
    template = {
        "千咲": {"en": "Chisa"},
    }
    with pytest.raises(ValueError) as exc:
        get_character_zh_and_en_name("葉瞬光", template)
    assert "Unknown character name" in str(exc.value)