import numpy as np
import json
import os

class ACAS_Engine:
    def __init__(self):
        self.profile_path = "data/security/rhythm_profile.json"
        os.makedirs("data/security", exist_ok=True)
        self.golden_profile = self._load_profile()
        self.trust_score = 100.0

    def _load_profile(self):
        if os.path.exists(self.profile_path):
            with open(self.profile_path, 'r') as f:
                return json.load(f)
        return None

    def enroll_user(self, rhythm_data: list):
        """Saves the initial Golden Rhythm profile."""
        with open(self.profile_path, 'w') as f:
            json.dump(rhythm_data, f, indent=4)
        self.golden_profile = rhythm_data
        return "Neural Rhythm Enrolled Successfully."

    def verify_rhythm(self, current_rhythm: list):
        """Compares current keystroke timings with the golden profile."""
        if not self.golden_profile:
            return 100 # No profile yet
        
        # Simple Manhattan Distance comparison for MVP
        # In production, we'd use a One-Class SVM or Isolation Forest
        try:
            golden_avg = np.mean([item['dwell'] for item in self.golden_profile])
            current_avg = np.mean([item['dwell'] for item in current_rhythm])
            
            diff = abs(golden_avg - current_avg)
            penalty = min(60, diff / 5) # Scale penalty
            
            self.trust_score = max(0, 100 - penalty)
            return self.trust_score
        except:
            return 50 # Error fallback

acas_engine = ACAS_Engine()
