from domain.echo.ocr_parser import parse_ocr_output, parse_stat_pair, PERCENTABLE

def test_parse_ocr_output_basic():
    """
    Parse OCR output into EchoData.

    Input contract:
    - 主詞條的名稱與數值會分兩行輸入:
        ["暴擊", "22%"]
    - 副詞條則是以一行為單位，透過冒號分隔名稱與數值
        ["生命:1500", "攻擊:11.6%"]

    Example:
        ocr_result = [
            "暴擊",
            "22%",
            "生命:1500",
            "攻擊:11.6%",
        ]
    """
    ocr = [
        "暴擊",
        "22%",
        "生命:1500",
        "攻擊:11.6%",
    ]

    echo = parse_ocr_output(ocr)

    assert echo.main_stat.name == "暴擊"
    assert echo.main_stat.value == 22
    assert echo.static_stat.name == "生命"
    assert echo.static_stat.value == 1500

    assert len(echo.sub_stat) == 1
    assert echo.sub_stat[0].name == "攻擊%"
    assert echo.sub_stat[0].value == 11.6


def test_parse_stat_pair_percent():
    name, value = parse_stat_pair("生命", "12.3%", PERCENTABLE)
    assert name == "生命%"
    assert value == 12.3

def test_parse_stat_pair_crit():
    name, val = parse_stat_pair("暴擊", "+7.0%", PERCENTABLE)
    assert name == "暴擊"
    assert val == 7.0