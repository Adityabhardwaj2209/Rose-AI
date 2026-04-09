from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
import os
from app_controller import app_controller
from vision_module import vision
from automation_agent import automation_agent
from memory_store import memory_store
from music_module import music_module
from recorder_tool import recorder_tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from weather_service import weather_service
from security_subsystem import security_subsystem
from emotion_analyzer import emotion_analyzer
from productivity_tracker import productivity_tracker
from aviation_radar import aviation_radar
from cosmic_radar import cosmic_radar
from cyber_shield_agent import cyber_shield
from knowledge_graph import knowledge_graph
from scenario_simulator import scenario_simulator
from reality_engine import reality_engine
from meta_guardian import meta_guardian

class BrainEngine:
    def __init__(self):
        # The Omega Swarm (UPI)
        self.radar = aviation_radar
        self.cosmic = cosmic_radar
        self.guardian = cyber_shield
        self.graph = knowledge_graph
        self.simulator = scenario_simulator
        self.reality = reality_engine
        self.meta = meta_guardian
        
        self.weather = weather_service
        self.ledger = smart_ledger
        self.tracker = productivity_tracker
        self.empathy = emotion_analyzer
        
        # Inject LLM into simulators
        self.reality.llm = self.llm
        self.simulator.llm = self.llm
        
        self.risky_keywords = ["whatsapp", "password", "delete", "payment"]
        
        # ... rest of init ...

    def _initialize_tools(self):
        return [
            "weather: Get latest weather",
            "search: Find information on the web",
            "app_launch: Open local apps",
            "finance: Scan bills and log items",
            "productivity: Analyze study hours",
            "airspace: Scan local skies",
            "cosmic: Track orbital satellites",
            "security: Neural network guardian"
        ]

    async def reason(self, user_input: str, image_data: str = None):
        lower_input = user_input.lower()
        
        # 0. Emergency & Security Overrides (Iron Citadel)
        if self.kill_switch in lower_input:
            return {"response": "PROTOCOL RADHA ACTIVATED.", "action": "INSTANT_LOCK", "emotion": "surprised"}
        
        # 1. Physical Home Control (IoT Hub)
        if "light" in lower_input or "home" in lower_input:
            # RBIAE: Pre-flight check
            mode = self.risk.get_permissibility("iot", {"network": "authorized"})
            if mode == "2FA":
                return {"response": "SYSTEM STRICT: Verify your Voice-Code to change environment settings, dude.", "action": "VOICE_CODE_CHALLENGE", "emotion": "surprised"}
            
            resp = self.iot.set_lights("on" in lower_input)
            return {"response": resp, "action": "iot_update", "emotion": "smiling"}

        # 2. Executive Management (G-Workspace)
        if "email" in lower_input or "mail" in lower_input:
            mode = self.risk.get_permissibility("email", {"network": "authorized"})
            if mode == "2FA":
                return {"response": "SYSTEM STRICT: High-risk zone detected. Verify Voice-Code to access emails.", "action": "VOICE_CODE_CHALLENGE", "emotion": "surprised"}
            
            emails = self.exec.get_unread_emails()
            return {"response": f"You've got {len(emails)} unread emails. Should I brief you?", "action": "email_report", "emotion": "smiling"}
        
        if "schedule" in lower_input or "calendar" in lower_input:
            events = self.exec.get_upcoming_events()
            return {"response": f"Strategic Schedule Check: You've got {len(events)} events coming up.", "action": "calendar_report", "emotion": "smiling"}

        # 3. Universal Intelligence Sensors (Radar, Cosmic, Security)
        if "iss" in lower_input:
            return {"response": "Tracking ISS...", "action": "cosmic_report"}

        # 0. Omega Presence - Confidence Calc
        confidence = self.reality.calculate_confidence(user_input)
        
        # Neural Processing
        memory_store.learn_habit("voice_command")
        
        # 1. Empathy Engine - Tone Analysis
        stress_level = self.empathy.analyze_voice_text(user_input)
        is_burning_out = self.empathy.get_burnout_warning()
        
        emotion = "neutral"
        if stress_level == "stressed": emotion = "surprised"

        # 2. Handshake / Proactive Greeting
        if "greet_user" in lower_input:
            import datetime
            hour = datetime.datetime.now().hour
            greeting = "Good morning" if 5 <= hour < 12 else "Good afternoon" if 12 <= hour < 18 else "Good evening"
            
            # Productivity context
            category, title = self.tracker.get_active_app()
            status_msg = f" I see you're in '{category}' mode with {title}."
            
            if is_burning_out:
                status_msg += " Listen, dude, you've been pushing hard. Take a 5 min break? I've got your back."
            
            return {
                "response": f"{greeting}, dude! I've initialized your Neural Link.{status_msg} What's our move?",
                "action": "greeting",
                "emotion": "smiling" if not is_burning_out else "thinking"
            }

        # 3. Risk Governance & Scenario Simulation
        if any(word in lower_input for word in self.risky_keywords):
            # Run Virtual Simulation
            best_case = await self.simulator.simulate_outcome(user_input)
            return {
                "response": f"Yo, that involves {user_input}. Before I touch that, I ran a neural simulation. Here's what could happen:\n\n{best_case}\n\nAre you sure you want me to handle this?",
                "action": "CONFIRMATION_REQUIRED",
                "emotion": "surprised"
            }

        # 4. Intelligence Tools (Cosmic, Security, Finance)
        if "bill" in lower_input or "scan" in lower_input:
             return {"response": "Got it. Hold the bill steady and I'll log it for you.", "action": "OCR_FINANCE", "emotion": "thinking"}

        if "iss" in lower_input or "satellite" in lower_input:
            pos = self.cosmic.get_iss_position()
            return {"response": f"Tracking cosmic orbiters... {pos['summary']}", "action": "cosmic_report", "emotion": "surprised"}

        if "security" in lower_input or "scan" in lower_input:
            threats = self.guardian.monitor_network()
            if not threats:
                return {"response": "Neural Guardian: Your system is secure. No suspicious activity detected.", "action": "security_report", "emotion": "smiling"}
            else:
                for threat in threats:
                    self.guardian.terminate_threat(threat['pid'])
                return {"response": "ALERT: Suspicious activity intercepted! malicious connections killed. We're safe, dude.", "action": "security_alert", "emotion": "surprised"}

        if "productivity" in lower_input or "study" in lower_input:
            cat, app = self.tracker.get_active_app()
            return {"response": f"You're currently in {cat} mode with {app}.", "action": "status_report", "emotion": "smiling"}

        # 5. The Thinking Loop (Inner Dialogue Pass)
        # Rose generates a response, then critiques it silently for peak iQ
        if self.llm:
            # We use the pure LLM call to get the most thoughtful response
            final_resp = await self.llm.ainvoke(f"{user_input}. Be casual and chill like Rose.")
            return {
                "response": final_resp.content,
                "action": "command_complete",
                "emotion": "smiling"
            }

        return {
            "response": "I've processed your request, dude.",
            "action": "command_complete",
            "emotion": "smiling"
        }


        # 4. Free News Search (DuckDuckGo)
        if "news" in lower_input or "world topic" in lower_input:
            emotion = "thinking"
            try:
                search_query = user_input.replace("news", "").strip() or "latest world news today"
                results = self.search.run(search_query)
                return {
                    "response": f"Yo, I checked the latest for you. Here's what's happening: {results[:500]}...",
                    "action": "news_search",
                    "emotion": "smiling"
                }
            except Exception as e:
                print(f"Search error: {e}")
                return {"response": "Man, my news feed is a bit jammed right now. Give me a sec?", "action": "none", "emotion": "neutral"}

        # 3. Llama 3 (Groq) if available
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

        # 4. Manual Fallbacks (When API keys are missing or failing)
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




