import os

class EmotionAnalyzer:
    def __init__(self):
        self.burnout_threshold = 5 # Number of stressed triggers
        self.stress_count = 0

    def analyze_voice_text(self, text: str):
        """Analyzes sentiment from transcription."""
        text = text.lower()
        stress_indicators = ["tired", "exhausted", "done", "stress", "fuck", "hate", "hard", "work", "boring"]
        
        score = sum(1 for word in stress_indicators if word in text)
        
        if score > 2:
            self.stress_count += 1
            return "stressed"
        elif score > 0:
            return "mildly_stressed"
        return "neutral"

    def get_burnout_warning(self):
        if self.stress_count >= self.burnout_threshold:
            self.stress_count = 0 # Reset
            return True
        return False

emotion_analyzer = EmotionAnalyzer()
