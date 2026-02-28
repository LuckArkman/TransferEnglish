import random
import time
from typing import Optional, List
from app.schemas.pressure import PressureChallenge, PressureSessionConfig

class PressureEngine:
    """
    Orchestrates "Testes Relâmpago" (Flash Tests) during a conversation.
    These are high-pressure, short-duration tasks designed to force automaticity.
    """

    def __init__(self):
        # Sample bank of pressure challenges (in practice, these would be dynamic)
        self.challenges_bank = [
            {"text": "I need to call my manager right now.", "label": "Social Action"},
            {"text": "The problem is related to the project budget.", "label": "Project Status"},
            {"text": "Can we schedule a meeting for next Tuesday?", "label": "Planning"},
            {"text": "I completely forgot about the decision we made.", "label": "Past Event"},
            {"text": "Could you repeat the last part of the presentation?", "label": "Clarification"},
        ]

    def trigger_challenge(self) -> PressureChallenge:
        """
        Picks a random challenge and generates a config.
        """
        challenge_data = random.choice(self.challenges_bank)
        import uuid
        return PressureChallenge(
            id=str(uuid.uuid4()),
            target_text=challenge_data["text"],
            time_limit_seconds=10, # Strict limit
            difficulty_multiplier=1.5,
            description=f"Quick Response Challenge: {challenge_data['label']}"
        )

    def evaluate_performance(
        self, 
        actual_response_time: float, 
        limit: int, 
        accuracy: float
    ) -> float:
        """
        Calculates a multiplier based on pressure performance.
        High accuracy + Low latency during pressure = Bonus IFP.
        """
        if actual_response_time > limit:
            return 0.5 # Fail or huge penalty
            
        time_factor = (limit - actual_response_time) / limit
        return (accuracy / 100.0) * (1.0 + time_factor)

pressure_engine = PressureEngine()
