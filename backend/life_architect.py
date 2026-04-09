import json
import os
from datetime import datetime

class LifeArchitect:
    def __init__(self):
        self.strategy_path = "data/strategy/life_vision.json"
        os.makedirs("data/strategy", exist_ok=True)
        self.vision = self._load_vision()

    def _load_vision(self):
        if os.path.exists(self.strategy_path):
            with open(self.strategy_path, 'r') as f:
                return json.load(f)
        return {
            "mission": "Lifelong Mastery & Universal Growth",
            "milestones": [],
            "current_focus": "Foundation Building",
            "narrative_arc": "The architect of their own destiny."
        }

    def add_milestone(self, goal: str, target_date: str):
        self.vision["milestones"].append({
            "goal": goal,
            "target": target_date,
            "status": "IN_PROGRESS"
        })
        self._save_vision()

    def get_todays_narrative(self):
        """Generates a supportive mentor-style narrative for current progress."""
        now = datetime.now().strftime("%Y-%m-%d")
        return f"Today, {now}, every small win is a brick in the monument of your lifelong vision. Stay focused, stay kind to yourself."

    def _save_vision(self):
        with open(self.strategy_path, 'w') as f:
            json.dump(self.vision, f, indent=4)

life_architect = LifeArchitect()
