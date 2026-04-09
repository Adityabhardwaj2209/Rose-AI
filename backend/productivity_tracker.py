import pygetwindow as gw
import psutil
import time
import json
import os
from datetime import datetime

class ProductivityTracker:
    def __init__(self):
        self.log_path = "data/productivity/daily_log.json"
        os.makedirs("data/productivity", exist_ok=True)
        self.active_apps = {
            "Study": ["code", "vscode", "terminal", "powershell", "browser", "notion"],
            "Procrastination": ["youtube", "netflix", "discord", "game"]
        }

    def get_active_app(self):
        """Identifies the currently active window title."""
        try:
            active_window = gw.getActiveWindow()
            if active_window:
                title = active_window.title.lower()
                for category, keywords in self.active_apps.items():
                    if any(key in title for key in keywords):
                        return category, active_window.title
                return "Neutral", active_window.title
            return "Idle", "None"
        except Exception:
            return "Idle", "None"

    def log_session(self, duration_seconds: int = 60):
        """Mocks a session logging logic."""
        category, title = self.get_active_app()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        entry = {
            "time": timestamp,
            "category": category,
            "app": title,
            "duration": duration_seconds
        }
        
        # In a real scenario, we append to a list and save daily
        print(f"Productivity Log: {category} - {title}")
        return entry

productivity_tracker = ProductivityTracker()
