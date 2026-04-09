import pygetwindow as gw
import time
import threading

class FocusGovernor:
    def __init__(self, app_controller=None):
        self.distractions = ["instagram", "youtube", "netflix", "facebook", "twitter"]
        self.focus_mode_active = False
        self.app_controller = app_controller
        self.is_active = True
        self._start_engine()

    def _start_engine(self):
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

    def _monitor_loop(self):
        """Active monitoring of attention DRIFT."""
        while self.is_active:
            if self.focus_mode_active:
                try:
                    active_window = gw.getActiveWindow()
                    if active_window:
                        title = active_window.title.lower()
                        if any(d in title for d in self.distractions):
                             # DRIFT DETECTED
                             print(f"Focus Governor: Attention drift detected in '{title}'. Steering back...")
                             # In a real impl, we'd trigger a supportive voice nudge and close the app
                             # self.app_controller.kill_process_by_name(title)
                except Exception as e:
                    pass
            time.sleep(30) # Check every 30s

    def set_focus_mode(self, active: bool):
        self.focus_mode_active = active
        return f"Focus Mode: {'ENABLED. I will protect your attention, dude.' if active else 'DISABLED.'}"

focus_governor = FocusGovernor()
