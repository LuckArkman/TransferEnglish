from sqlalchemy.orm import Session
from app.core.db.session import SessionLocal
from app.models.gamification import Achievement
from app.models.content import ScenarioTemplate
from app.models.linguistics import Cognate, CognateType

def seed_data():
    db: Session = SessionLocal()
    try:
        # 1. Seed Achievements
        if db.query(Achievement).count() == 0:
            achievements = [
                Achievement(name="First Contact", description="Complete your first conversation session.", criteria_type="sessions_count", criteria_value=1, icon="🎯"),
                Achievement(name="Consistency King", description="Complete 10 conversation sessions.", criteria_type="sessions_count", criteria_value=10, icon="👑"),
                Achievement(name="Speed Demon", description="Achieve a response latency under 1.5s in 5 missions.", criteria_type="latency", criteria_value=1.5, icon="⚡"),
            ]
            db.add_all(achievements)
            print("Seeded Achievements.")

        # 2. Seed Scenarios
        if db.query(ScenarioTemplate).count() == 0:
            scenarios = [
                ScenarioTemplate(
                    title="The Job Interview",
                    description="Simulate a formal job interview for a Tech Lead position.",
                    level="advanced",
                    config={
                        "persona": "Senior HR Manager",
                        "tone": "formal",
                        "objectives": ["introduce yourself", "explain your background", "negotiate salary expectations"]
                    }
                ),
                ScenarioTemplate(
                    title="Coffee Shop Ordering",
                    description="Order a coffee and a snack in a busy NYC Starbucks.",
                    level="beginner",
                    config={
                        "persona": "Busy Barista",
                        "tone": "casual",
                        "objectives": ["order a latte", "mention a food allergy", "pay with credit card"]
                    }
                ),
            ]
            db.add_all(scenarios)
            print("Seeded Scenarios.")

        # 3. Seed Basic Cognates
        if db.query(Cognate).count() == 0:
            cognates = [
                {"name": "Future", "portuguese": "Futuro", "type": "identical", "difficulty_level": "beginner"},
                {"name": "Important", "portuguese": "Importante", "type": "near_identical", "difficulty_level": "beginner"},
                {"name": "Different", "portuguese": "Diferente", "type": "near_identical", "difficulty_level": "beginner"},
                {"name": "Problem", "portuguese": "Problema", "type": "near_identical", "difficulty_level": "beginner"},
                {"name": "Idea", "portuguese": "Ideia", "type": "identical", "difficulty_level": "beginner"},
            ]
            for c in cognates:
                db.add(Cognate(**c, tenant_id="default-tenant"))
            print("Seeded Cognates.")

        db.commit()
    except Exception as e:
        print(f"Error seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
