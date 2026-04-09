import subprocess
import os

class AppController:
    def __init__(self):
        # Common app names to executable paths/commands
        self.apps = {
            "chrome": ["start", "chrome"],
            "vs code": ["code"],
            "notedpad": ["notepad"],
            "discord": ["start", "discord"],
            "calculator": ["calc"],
            "file explorer": ["explorer"]
        }

    def launch(self, app_name: str):
        app_name = app_name.lower()
        
        # Check standard apps
        if app_name in self.apps:
            try:
                subprocess.Popen(self.apps[app_name], shell=True)
                return f"Opening {app_name} for you, dude."
            except Exception as e:
                return f"My bad, couldn't open {app_name}. Error: {str(e)}"
        
        # Fallback to generic start command
        try:
            subprocess.Popen(["start", app_name], shell=True)
            return f"Trying to launch {app_name}..."
        except:
            return f"Sorry man, no idea what {app_name} is. You got it installed?"

app_controller = AppController()
