import cv2
import mediapipe as mp
import pyautogui
import threading
import time

class NeuralInterface:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_face = mp.solutions.face_mesh
        self.face = self.mp_face.FaceMesh(refine_landmarks=True)
        self.mp_draw = mp.solutions.drawing_utils
        
        self.is_active = False
        self.screen_w, self.screen_h = pyautogui.size()
        pyautogui.FAILSAFE = True # Corner-of-screen exit

    def start_engine(self):
        self.is_active = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        return "Neural Interface Active. Finger-tracking and Blink-click engaged."

    def _run_loop(self):
        cap = cv2.VideoCapture(0)
        while self.is_active:
            success, image = cap.read()
            if not success: continue
            
            image = cv2.flip(image, 1)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # 1. Hand Tracking (Finger Cursor)
            hand_results = self.hands.process(rgb_image)
            if hand_results.multi_hand_landmarks:
                for hand_lms in hand_results.multi_hand_landmarks:
                    index_tip = hand_lms.landmark[8]
                    x = int(index_tip.x * self.screen_w)
                    y = int(index_tip.y * self.screen_h)
                    pyautogui.moveTo(x, y, duration=0.1, _pause=False)
                    
                    # Palm Detection (Open HUD)
                    # Coordinates for fingers being up
                    fingers = [8, 12, 16, 20]
                    up_count = sum(1 for f in fingers if hand_lms.landmark[f].y < hand_lms.landmark[f-2].y)
                    if up_count >= 4:
                        # Event: Palm Up -> Open App
                        pass

            # 2. Face Mesh (Blink Click)
            face_results = self.face.process(rgb_image)
            if face_results.multi_face_landmarks:
                for face_lms in face_results.multi_face_landmarks:
                    # Eye Blink detection (Landmarks 145 and 159 for left eye)
                    left_eye_top = face_lms.landmark[159].y
                    left_eye_bottom = face_lms.landmark[145].y
                    if (left_eye_bottom - left_eye_top) < 0.004:
                         pyautogui.click()
                         time.sleep(0.5) # Debounce

            time.sleep(0.01)
        cap.release()

neural_interface = NeuralInterface()
