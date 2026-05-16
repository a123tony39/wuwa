from backend.domain.score.score import get_rank

def test_rank_mid_values():
    assert get_rank(85) == "SS"
    assert get_rank(75) == "S"
    assert get_rank(65) == "A"
    assert get_rank(55) == "B"
    assert get_rank(10) == "F"

def test_rank_boundaries():
    assert get_rank(80) == "SS"
    assert get_rank(79) == "S"

    assert get_rank(70) == "S"
    assert get_rank(69) == "A"

    assert get_rank(60) == "A"
    assert get_rank(59) == "B"

    assert get_rank(50) == "B"
    assert get_rank(49) == "F"