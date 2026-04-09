import pytesseract
from PIL import Image
import pyautogui
import os
import time

class VisionModule:
    def __init__(self, tesseract_cmd=None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        elif os.name == 'nt':
            # Default path for Tesseract on Windows
            potential_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            if os.path.exists(potential_path):
                pytesseract.pytesseract.tesseract_cmd = potential_path

    def capture_screen(self, filename="screenshot.png"):
        """Captures the full screen and saves it temporarily."""
        screens_dir = "data/screenshots"
        os.makedirs(screens_dir, exist_ok=True)
        path = os.path.join(screens_dir, filename)
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        return path

    def extract_text(self, image_path: str):
        try:
            image = Image.open(image_path)
            # Use specific config for better results with Tesseract
            text = pytesseract.image_to_string(image, config='--psm 6')
            return text
        except Exception as e:
            return f"Error during OCR: {str(e)}"

    def see_and_tell(self):
        """High-level tool: Capture screen and extract all text."""
        path = self.capture_screen()
        text = self.extract_text(path)
        return {"text": text, "image_path": path}

vision = VisionModule()

