import os
import numpy as np
import librosa
from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path

class SecuritySubsystem:
    def __init__(self):
        self.encoder = VoiceEncoder()
        self.profile_path = "data/security/voice_profile.npy"
        os.makedirs("data/security", exist_ok=True)
        self.current_profile = self._load_profile()

    def _load_profile(self):
        if os.path.exists(self.profile_path):
            return np.load(self.profile_path)
        return None

    def enroll_voice(self, audio_path: str):
        """Creates a unique voice fingerprint from an audio sample."""
        try:
            wav = preprocess_wav(audio_path)
            embedding = self.encoder.embed_utterance(wav)
            np.save(self.profile_path, embedding)
            self.current_profile = embedding
            return True
        except Exception as e:
            print(f"Enrollment Error: {e}")
            return False

    def verify_voice(self, audio_path: str, threshold: float = 0.75):
        """Compares a live voice sample against the stored fingerprint."""
        if self.current_profile is None:
            return True # No profile yet, proceed with caution
        
        try:
            wav = preprocess_wav(audio_path)
            live_embedding = self.encoder.embed_utterance(wav)
            
            # Use Cosine Similarity
            similarity = np.dot(self.current_profile, live_embedding) / (
                np.linalg.norm(self.current_profile) * np.linalg.norm(live_embedding)
            )
            
            print(f"Voice Match Similarity: {similarity:.4f}")
            return similarity >= threshold
        except Exception as e:
            print(f"Verification Error: {e}")
            return False

security_subsystem = SecuritySubsystem()
