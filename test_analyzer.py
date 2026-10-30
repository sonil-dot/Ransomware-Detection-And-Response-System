
from analyzer import calculate_threat_score


def test_low_file_activity():
    score = calculate_threat_score(2, 3.0)
    assert score == 0


def test_moderate_file_activity():
    score = calculate_threat_score(10, 3.0)
    assert score == 40


def test_high_file_activity():
    score = calculate_threat_score(20, 3.0)
    assert score == 70


def test_high_entropy():
    score = calculate_threat_score(0, 7.5)
    assert score == 20


def test_maximum_score():
    score = calculate_threat_score(20, 7.5)
    assert score == 90
