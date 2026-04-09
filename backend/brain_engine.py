from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import Tool


import os
from app_controller import app_controller
from vision_module import vision
from automation_agent import automation_agent
from memory_store import memory_store
from music_module import music_module
from recorder_tool import recorder_tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class BrainEngine:
    def __init__(self):
        # The Reasoning Engine (Llama 3 via Groq)
        self.llm = ChatGroq(
            model_name="llama3-70b-8192",
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.7
        ) if os.getenv("GROQ_API_KEY") else None

        # The Vision Engine (Gemini)
        self.vision_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        ) if os.getenv("GOOGLE_API_KEY") else None
        
        self.tools = self._initialize_tools()

    def _initialize_tools(self):
        # We'll use manual tool mapping for now to avoid LangChain version conflicts
        return []

    async def reason(self, user_input: str, image_data: str = None):
        # Store in memory first
        memory_store.learn_habit("voice_command")
        
        # Talking Tom Effect - Behaviour Sensing
        lower_input = user_input.lower()
        emotion = "neutral"
        
        # Handle Multimodal Input (Camera)
        processed_image_text = ""
        if image_data:
            # Save base64 image and extract text
            import base64
            from io import BytesIO
            from PIL import Image
            
            try:
                header, encoded = image_data.split(",", 1)
                data = base64.b64decode(encoded)
                img = Image.open(BytesIO(data))
                path = "data/screenshots/camera_snapshot.png"
                img.save(path)
                processed_image_text = vision.extract_text(path)
                print(f"Rose saw: {processed_image_text}")
            except Exception as e:
                print(f"Vision error: {e}")

        # Identity & System Persona
        system_prompt = (
            "You are Rose, a stunningly beautiful and hyper-intelligent AI assistant. "
            "You are a loyal friend, laid back, and use casual language (yo, dude, man, gotchu). "
            "You have a chill female persona. You can SEE the screen, AUTOMATE the system, and PLAY MUSIC."
        )

        # 1. Use Llama 3 (Groq) if available
        if self.llm:
            try:
                # Advanced reasoning with Llama 3
                ai_msg = self.llm.invoke([
                    ("system", system_prompt),
                    ("human", user_input)
                ])
                return {
                    "response": ai_msg.content,
                    "action": "llama_reasoning",
                    "emotion": "smiling" if "happy" in ai_msg.content.lower() else "neutral"
                }
            except Exception as e:
                print(f"Llama 3 error: {e}")

        # 2. Manual Fallbacks (When API keys are missing or failing)
        if not os.getenv("GOOGLE_API_KEY") or not self.llm:
            # Look at me / Vision fallback
            if "look at me" in lower_input or "see me" in lower_input:
                return {
                    "response": f"Yo, I'm checking you out with my Llama 3 brain... Oh wait, I need a vision key for that. But you sound chill!",
                    "action": "camera_vision",
                    "emotion": "smiling"
                }

            if "record" in lower_input or "capture video" in lower_input:
                res = recorder_tool.trigger_recording()
                return {"response": res['message'], "action": res['instruction'], "emotion": "neutral"}

            if "play" in lower_input or "song" in lower_input:
                res = music_module.identify_and_play(user_input)
                app_controller.launch(res['url'])
                return {"response": res['message'], "action": "music_playback", "emotion": "smiling"}

            if "open" in lower_input or "launch" in lower_input:
                for app in app_controller.apps:
                    if app in lower_input:
                        return {"response": app_controller.launch(app), "action": "app_launch", "emotion": "neutral"}
            
            return {
                "response": f"Yo, I'd totally help you with '{user_input}', but my API key is missing. Add it to .env so we can vibe properly.",
                "action": "none",
                "emotion": "neutral"
            }
        
        # Real reasoning would dynamically assign the best emotion based on sentiment analysis
        return {"response": f"Gotchu, dude. I'm on it.", "action": "planning", "emotion": emotion}

brain = BrainEngine()




