"use client";

import { motion } from "framer-motion";
import { Shield, Fingerprint, Keyboard } from "lucide-react";
import { useState, useRef } from "react";

export default function AuthPulse({ onComplete }: { onComplete: () => void }) {
  const [typed, setTyped] = useState("");
  const [data, setData] = useState<any[]>([]);
  const lastKeyTime = useRef<number>(Date.now());
  const phrase = "the quick brown fox jumps over the lazy dog";

  const handleKeyDown = (e: React.KeyboardEvent) => {
    const now = Date.now();
    const dwell = 50; // Approximated for MVP
    const flight = now - lastKeyTime.current;
    
    setData([...data, { key: e.key, flight, dwell }]);
    lastKeyTime.current = now;
  };

  const handleInput = (e: any) => {
    const val = e.target.value;
    setTyped(val);
    if (val === phrase) {
      submitEnrolment();
    }
  };

  const submitEnrolment = async () => {
    await fetch("http://localhost:8000/api/enroll_rhythm", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rhythm: data }),
    });
    onComplete();
  };

  return (
    <motion.div 
      initial={{ opacity: 0 }} 
      animate={{ opacity: 1 }}
      className="fixed inset-0 z-[1000] bg-[#020617]/95 backdrop-blur-xl flex items-center justify-center p-8"
    >
      <div className="max-w-xl w-full flex flex-col items-center gap-8 text-center">
        <div className="p-4 glass rounded-3xl border border-cyan-400/20 shadow-[0_0_30px_rgba(34,211,238,0.2)]">
           <Fingerprint className="w-12 h-12 text-cyan-400 animate-pulse" />
        </div>
        
        <div>
          <h2 className="text-2xl font-bold tracking-widest text-white uppercase">Neural Rhythm Enrollment</h2>
          <p className="text-sm text-white/40 mt-2">Type the phrase below to establish your unique biometric signature.</p>
        </div>

        <div className="w-full glass p-8 rounded-3xl border border-white/5 relative group">
           <p className="text-xl font-mono text-cyan-400/50 mb-6 select-none">{phrase}</p>
           <input
             autoFocus
             value={typed}
             onKeyDown={handleKeyDown}
             onChange={handleInput}
             className="w-full bg-white/5 border-b-2 border-cyan-400/50 p-4 text-2xl text-white font-mono focus:outline-none focus:border-cyan-400 transition-all text-center"
             placeholder="START TYPING..."
           />
           <div className="mt-4 flex justify-between text-[10px] uppercase tracking-widest text-white/20">
             <span>Capturing Latency...</span>
             <span>Dwell Scan...</span>
             <span>Context Locked</span>
           </div>
        </div>
      </div>
    </motion.div>
  );
}
