import unittest
from datetime import date, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Goal, SubGoal, Task
from app.services.goal_service import get_progress
from app.services.recommendations import daily_tasks
from app.services.scheduler import schedule_tasks


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.db = self.Session()

        goal = Goal(
            title="Learn Python",
            deadline=date.today() + timedelta(days=3),
            available_hours_per_day=2,
        )
        self.db.add(goal)
        self.db.flush()
        subgoal = SubGoal(goal_id=goal.id, title="Python Basics")
        self.db.add(subgoal)
        self.db.flush()
        self.db.add(Task(subgoal_id=subgoal.id, title="Variables", estimated_minutes=30))
        self.db.add(Task(subgoal_id=subgoal.id, title="Functions", estimated_minutes=60))
        self.db.commit()
        self.goal = goal

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def test_schedule_assigns_dates(self):
        tasks = schedule_tasks(self.db, self.goal)
        self.assertEqual(len(tasks), 2)
        self.assertTrue(all(task.scheduled_date for task in tasks))

    def test_progress(self):
        task = self.goal.subgoals[0].tasks[0]
        task.status = "completed"
        self.db.commit()
        progress = get_progress(self.db, self.goal.id)
        self.assertEqual(progress["total_tasks"], 2)
        self.assertEqual(progress["completed_tasks"], 1)
        self.assertEqual(progress["progress_percentage"], 50.0)

    def test_daily_recommendations(self):
        schedule_tasks(self.db, self.goal)
        tasks = daily_tasks(self.db, self.goal.id, date.today())
        self.assertGreaterEqual(len(tasks), 1)


if __name__ == "__main__":
    unittest.main()
