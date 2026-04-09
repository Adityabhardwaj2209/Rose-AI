import os
import time

class RecorderTool:
    def __init__(self):
        self.recordings_dir = "data/recordings"
        os.makedirs(self.recordings_dir, exist_ok=True)

    def trigger_recording(self, duration: int = 10):
        """Instructions for the frontend to record camera/screen."""
        # Note: Actual recording happens in the browser via MediaRecorder API
        return {
            "instruction": "START_RECORDING",
            "duration": duration,
            "filename": f"rose_record_{int(time.time())}.webm",
            "message": f"Sure thing! I'm starting a {duration} second recording of our session now."
        }

recorder_tool = RecorderTool()
