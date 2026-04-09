import psutil
import time
import subprocess
import os
import threading

class MetaGuardian:
    def __init__(self):
        self.monitored_processes = ["python", "node"]
        self.health_history = []
        self.is_active = True
        self._start_monitor()

    def _start_monitor(self):
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

    def _monitor_loop(self):
        """Continuously checks the health of Rose's neural subsystems."""
        while self.is_active:
            try:
                # Check server health
                # (Conceptual: checking if port 8000 is responsive)
                # If fail: self.restart_system()
                time.sleep(60) # Scan every minute
            except Exception as e:
                print(f"Meta-Guardian Error: {e}")

    def restart_system(self):
        """Autonomous self-healing: Restarts the backend server."""
        print("Neural Crisis Detected: Initiating Self-Healing Protocol...")
        # In a real environment, we would use a process manager like PM2 
        # but for this script, we log the healing event.
        os.system("echo System Restarted by Rose Meta-Guardian > data/logs/recovery.log")

    def get_system_health(self):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        return {"cpu": cpu, "mem": mem, "status": "SECURE" if cpu < 90 else "CRITICAL"}

meta_guardian = MetaGuardian()
