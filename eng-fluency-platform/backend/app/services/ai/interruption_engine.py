from typing import List, Optional, Dict
from app.schemas.phonetic import PhoneticAssessment
from app.models.linguistics import CognateType

class InterruptionEngine:
    """
    Decides when to provide pedagogical interventions during a conversation.
    Focuses on:
    1. False Cognates (critical errors)
    2. Persistent pronunciation errors (Phonetic Assessment)
    3. Structural Portuguese-to-English literal translations (Vícios)
    """

    def __init__(self):
        # List of critical patterns to watch for (Portuguese-isms)
        self.vicious_patterns = {
            "have a person": "there is a person",
            "for me to do": "for me to do (wait, this is okay, maybe 'to I do')",
            "is true": "it is true",
            "make a course": "take a course",
            "depend of": "depend on"
        }

    async def analyze(
        self, 
        text: str, 
        phonetic: Optional[PhoneticAssessment] = None
    ) -> Optional[Dict[str, str]]:
        """
        Returns a tip if an intervention is needed.
        """
        text_lower = text.lower()

        # Check for Vicious Patterns (Literal Translations)
        for pattern, correction in self.vicious_patterns.items():
            if pattern in text_lower:
                return {
                    "type": "grammar",
                    "title": "Natural Phrasing",
                    "message": f"In English, we usually say '{correction}' instead of '{pattern}'."
                }

        # Check for critical phonetic errors (Low accuracy on a specific word)
        if phonetic and phonetic.accuracy_score < 60:
            weak_words = [w for w in phonetic.words if w.accuracy_score < 50]
            if weak_words:
                target_word = weak_words[0].word
                return {
                    "type": "phonetic",
                    "title": "Pronunciation Tip",
                    "message": f"Let's try the word '{target_word}' again. Pay attention to the vowel sound."
                }

        return None

interruption_engine = InterruptionEngine()
