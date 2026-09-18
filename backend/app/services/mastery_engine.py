import math

class BKTMasteryEngine:
    \"\"\"
    Bayesian Knowledge Tracing (BKT) Engine
    Deterministic statistical state-update for cognitive mastery modeling.
    \"\"\"
    def __init__(
        self,
        p_transit: float = 0.15,
        p_guess: float = 0.25,
        p_slip: float = 0.10
    ):
        self.p_transit = p_transit
        self.p_guess = p_guess
        self.p_slip = p_slip

    def compute_posterior(self, prior_mastery: float, is_correct: bool) -> float:
        prior = max(0.001, min(0.999, prior_mastery))
        if is_correct:
            p_obs_given_known = 1.0 - self.p_slip
            p_obs_given_unknown = self.p_guess
            num = p_obs_given_known * prior
            denom = num + (p_obs_given_unknown * (1.0 - prior))
            p_learned_given_obs = num / denom
        else:
            p_obs_given_known = self.p_slip
            p_obs_given_unknown = 1.0 - self.p_guess
            num = p_obs_given_known * prior
            denom = num + (p_obs_given_unknown * (1.0 - prior))
            p_learned_given_obs = num / denom

        # Knowledge transition step
        new_mastery = p_learned_given_obs + (1.0 - p_learned_given_obs) * self.p_transit
        return round(float(new_mastery), 4)

    def classify_level(self, score: float) -> str:
        if score < 0.30:
            return "novice"
        elif score < 0.60:
            return "developing"
        elif score < 0.80:
            return "proficient"
        return "mastered"
