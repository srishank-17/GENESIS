import pytest
from app.services.mastery_engine import BKTMasteryEngine

def test_bkt_correct_answer_increases_mastery():
    engine = BKTMasteryEngine(p_transit=0.15, p_guess=0.25, p_slip=0.10)
    prior = 0.20
    posterior = engine.compute_posterior(prior_mastery=prior, is_correct=True)
    assert posterior > prior
    assert 0.0 <= posterior <= 1.0

def test_bkt_incorrect_answer_decreases_mastery():
    engine = BKTMasteryEngine(p_transit=0.15, p_guess=0.25, p_slip=0.10)
    prior = 0.50
    posterior = engine.compute_posterior(prior_mastery=prior, is_correct=False)
    assert posterior < prior

def test_bkt_classify_levels():
    engine = BKTMasteryEngine()
    assert engine.classify_level(0.15) == "novice"
    assert engine.classify_level(0.45) == "developing"
    assert engine.classify_level(0.72) == "proficient"
    assert engine.classify_level(0.92) == "mastered"
