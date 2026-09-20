import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.agent import GoalAgent
from app.models import Base, Goal, SubGoal, Task


class AgentTests(unittest.TestCase):
    def test_agent_creates_a_plan(self):
        engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        db = Session()
        try:
            goal = Goal(title="Learn FastAPI", available_hours_per_day=1)
            db.add(goal)
            db.commit()
            db.refresh(goal)

            result = GoalAgent().run(db, goal)

            self.assertEqual(result["subgoals_created"], 4)
            self.assertEqual(result["tasks_created"], 12)
            self.assertEqual(db.query(SubGoal).count(), 4)
            self.assertEqual(db.query(Task).count(), 12)
        finally:
            db.close()
            engine.dispose()


if __name__ == "__main__":
    unittest.main()
