"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Cpu, 
  Activity, 
  Globe, 
  Bell, 
  Settings, 
  Search, 
  Mic, 
  ShieldCheck, 
  BrainCircuit,
  Terminal,
  Volume2
} from "lucide-react";
import ThePersona from "@/components/ThePersona";
import CameraEye, { CameraEyeHandle } from "@/components/CameraEye";

export default function Home() {
  const [status, setStatus] = useState<"idle" | "thinking" | "speaking" | "listening">("idle");
  const [emotion, setEmotion] = useState<"neutral" | "smiling" | "surprised" | "thinking">("neutral");
  const [response, setResponse] = useState("YO, I'M ROSE. SAY SOMETHING!");
  const [isListening, setIsListening] = useState(false);
  
  const recognitionRef = useRef<any>(null);
  const cameraRef = useRef<CameraEyeHandle>(null);

  useEffect(() => {
    // Initialize Speech Recognition
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        handleCommand(transcript);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
        if (status === "idle") {
          // Restart listening if we're idle
          // setTimeout(() => startListening(), 1000);
        }
      };
    }
  }, []);

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      try {
        recognitionRef.current.start();
        setIsListening(true);
        setStatus("listening");
      } catch (e) {
        console.error("Mic error:", e);
      }
    }
  };

  const speak = (text: string) => {
    const utterance = new SpeechSynthesisUtterance(text);
    
    // Select the best female voice
    const voices = window.speechSynthesis.getVoices();
    const femaleVoice = voices.find(v => v.name.includes("Female") || v.name.includes("Google") || v.name.includes("Zira") || v.name.includes("Microsoft")) 
                         || voices.find(v => v.lang.startsWith("en-") && v.name.includes("Female"))
                         || voices[0];
    
    if (femaleVoice) {
      utterance.voice = femaleVoice;
    }

    utterance.pitch = 0.9; // Slightly lower for JARVIS feel
    utterance.rate = 1.0;

    utterance.onstart = () => setStatus("speaking");
    utterance.onend = () => {
      setStatus("idle");
      setTimeout(startListening, 500);
    };
    window.speechSynthesis.speak(utterance);
  };

  const handleCommand = async (commandText: string) => {
    if (!commandText.trim()) return;
    setStatus("thinking");
    setEmotion("thinking");
    setResponse(`PLANNING: ${commandText.toUpperCase()}`);
    
    // Capture snapshot if Rose needs to "see"
    let imageSnapshot = null;
    const isVisionCommand = commandText.toLowerCase().includes("look at me") || 
                            commandText.toLowerCase().includes("see me") ||
                            commandText.toLowerCase().includes("ocr");
                            
    if (isVisionCommand) {
      imageSnapshot = cameraRef.current?.capture();
    }
    
    try {
      const resp = await fetch("http://localhost:8000/api/command", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          text: commandText,
          image: imageSnapshot
        }),
      });
      const data = await resp.json();
      
      setResponse(data.response.toUpperCase());
      setEmotion(data.emotion || "neutral");
      speak(data.response);

      // Handle Special Tool Instructions
      if (data.action === "START_RECORDING") {
        startBrowserRecording();
      }
    } catch (error) {
      console.error("Link error:", error);
      setStatus("idle");
    }
  };

  const startBrowserRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getDisplayMedia({ video: true });
      const mediaRecorder = new MediaRecorder(stream);
      const chunks: BlobPart[] = [];
      
      mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: "video/webm" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "rose_memory_record.webm";
        a.click();
      };
      
      mediaRecorder.start();
      setTimeout(() => mediaRecorder.stop(), 5000); // Record 5 seconds
    } catch (err) {
      console.error("Recording failed:", err);
    }
  };

  return (
    <main className="relative h-screen w-screen flex flex-col items-center justify-center overflow-hidden">
      <CameraEye ref={cameraRef} />
      {/* Background FX */}
      <div className="scanline" />
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-purple-500/5 pointer-events-none" />

      {/* Top Bar */}
      <nav className="absolute top-0 w-full p-6 flex justify-between items-center glass z-10">
        <div className="flex items-center gap-4">
          <BrainCircuit className="text-cyan-400 w-8 h-8" />
          <h1 className="text-xl font-bold tracking-widest text-cyan-400">R.O.S.E. <span className="text-xs text-white/40 ml-2">v2.0</span></h1>
        </div>
        <div className="flex items-center gap-8">
          <div className="flex gap-4">
            <Stat icon={<Cpu />} label="CPU" value="12%" color="text-cyan-400" />
            <Stat icon={<Activity />} label="MEM" value="4.2GB" color="text-purple-400" />
            <Stat icon={<ShieldCheck />} label="SEC" value="ACTIVE" color="text-green-400" />
          </div>
          <Settings className="text-white/60 hover:text-white cursor-pointer transition-colors" />
        </div>
      </nav>

      {/* Left Sidebar - Agent Status */}
      <div className="absolute left-6 top-1/2 -translate-y-1/2 flex flex-col gap-4 z-10">
        <AgentBadge name="Research" active />
        <AgentBadge name="Coding" />
        <AgentBadge name="Guardian" active />
        <AgentBadge name="Career" />
      </div>

      {/* Right Sidebar - Recent Activity */}
      <div className="absolute right-6 top-1/2 -translate-y-1/2 w-64 glass p-4 rounded-xl flex flex-col gap-4 z-10">
        <h3 className="text-xs font-bold uppercase tracking-wider text-cyan-400 mb-2">Live Logs</h3>
        <div className="flex flex-col gap-3 h-96 overflow-y-auto pr-2 custom-scroll">
          <LogEntry time="19:22" text="System initialization complete." />
          <LogEntry time="19:23" text="Predictive Engine online." />
          <LogEntry time="19:24" text="Monitoring traffic patterns..." />
          <LogEntry time="19:25" text="Neural memory synchronized." />
        </div>
      </div>

      {/* Center - The Persona & Responses */}
      <div className="flex flex-col items-center gap-12 max-w-4xl text-center">
        <ThePersona status={status} emotion={emotion} />
        
        <div className="flex flex-col gap-4">
          <motion.p 
            animate={{ opacity: [0.4, 0.8, 0.4] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="text-cyan-400/80 tracking-[0.2em] font-medium text-sm"
          >
            {status === "idle" ? "READY" : status.toUpperCase()}
          </motion.p>
          
          <AnimatePresence mode="wait">
            <motion.h2 
              key={response}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="text-2xl md:text-4xl font-bold text-white tracking-tight leading-tight px-6"
            >
              "{response}"
            </motion.h2>
          </AnimatePresence>
        </div>
      </div>

      {/* Bottom - Voice Trigger & EQ */}
      <div className="absolute bottom-20 flex flex-col items-center gap-6 z-10">
        {status === "speaking" && (
          <div className="flex gap-1 items-end h-8">
            {[...Array(8)].map((_, i) => (
              <motion.div 
                key={i}
                animate={{ height: [4, 16 + Math.random() * 16, 4] }}
                transition={{ duration: 0.3, repeat: Infinity, delay: i * 0.05 }}
                className="w-1.5 bg-cyan-400 rounded-full"
              />
            ))}
          </div>
        )}
        
        <motion.button 
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={startListening}
          className={`w-20 h-20 rounded-full glass flex items-center justify-center border-2 transition-all shadow-[0_0_20px_rgba(34,211,238,0.2)] ${
            isListening ? 'border-red-500 bg-red-500/10' : 'border-cyan-400 bg-cyan-400/10'
          }`}
        >
          {isListening ? (
            <div className="flex gap-1 items-center">
              {[...Array(3)].map((_, i) => (
                <motion.div 
                  key={i}
                  animate={{ height: [8, 24, 8] }}
                  transition={{ duration: 0.5, repeat: Infinity, delay: i * 0.1 }}
                  className="w-1.5 bg-red-400 rounded-full"
                />
              ))}
            </div>
          ) : (
            <Mic className="text-cyan-400 w-8 h-8" />
          )}
        </motion.button>
        <p className="text-[10px] uppercase tracking-[0.3em] text-white/40">
          {isListening ? "Listening..." : "Tap to Speak"}
        </p>
      </div>
    </main>
  );
}

function Stat({ icon, label, value, color }: { icon: React.ReactNode, label: string, value: string, color: string }) {
  return (
    <div className="flex items-center gap-2 px-3 py-1 rounded-lg border border-white/5 bg-white/5">
      <div className={`w-4 h-4 ${color}`}>{icon}</div>
      <div className="flex flex-col leading-tight">
        <span className="text-[10px] text-white/40 uppercase">{label}</span>
        <span className="text-xs font-bold text-white/80">{value}</span>
      </div>
    </div>
  );
}

function AgentBadge({ name, active = false }: { name: string, active?: boolean }) {
  return (
    <div className={`glass px-4 py-2 rounded-lg border-l-4 transition-all ${active ? 'border-cyan-400 translate-x-1' : 'border-transparent opacity-40'}`}>
      <span className="text-xs font-bold tracking-widest uppercase">{name}</span>
    </div>
  );
}

function LogEntry({ time, text }: { time: string, text: string }) {
  return (
    <div className="flex flex-col gap-1">
      <span className="text-[10px] text-cyan-400 font-mono tracking-tighter">[{time}]</span>
      <p className="text-[11px] text-white/60 leading-relaxed font-mono">{text}</p>
    </div>
  );
}
