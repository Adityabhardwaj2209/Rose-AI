"use client";

import { motion, AnimatePresence } from "framer-motion";
import { useState, useEffect } from "react";

interface PersonaProps {
  status: "idle" | "thinking" | "speaking" | "listening";
  emotion?: "neutral" | "smiling" | "surprised" | "thinking";
}

export default function ThePersona({ status, emotion = "neutral" }: PersonaProps) {
  const [isBlinking, setIsBlinking] = useState(false);
  const isActive = status === "speaking" || status === "listening";

  // Natural Blinking Loop
  useEffect(() => {
    const blinkCycle = setInterval(() => {
      setIsBlinking(true);
      setTimeout(() => setIsBlinking(false), 200);
    }, Math.random() * 4000 + 3000);

    return () => clearInterval(blinkCycle);
  }, []);

  // Map Emotion to Image Path (Future-proofing for more assets)
  const getImagePath = () => {
    if (isBlinking) return "/assets/persona_blink.png";
    return "/assets/persona_neutral.png";
  };

  return (
    <div className="relative flex items-center justify-center w-[400px] h-[400px]">
      {/* Liquid Background Aura */}
      <motion.div
        animate={{
          scale: status === "speaking" ? [1, 1.15, 1] : isActive ? [1, 1.1, 1] : [1, 1.05, 1],
          opacity: isActive ? [0.4, 0.8, 0.4] : [0.2, 0.4, 0.2],
        }}
        transition={{
          duration: status === "speaking" ? 0.3 : isActive ? 2 : 4,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute inset-0 rounded-full blur-[60px]"
        style={{
          background: status === "listening" 
            ? "radial-gradient(circle, #22d3ee 0%, transparent 70%)"
            : status === "thinking"
            ? "radial-gradient(circle, #a855f7 0%, transparent 70%)"
            : "radial-gradient(circle, #22d3ee44 0%, transparent 70%)",
        }}
      />

      {/* Main Persona Container */}
      <div className="relative w-full h-full rounded-2xl overflow-hidden border border-white/10 glass shadow-2xl">
        <AnimatePresence mode="wait">
          <motion.div
            key={getImagePath()}
            initial={{ opacity: 0.8 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0.8 }}
            transition={{ duration: 0.1 }}
            className="w-full h-full"
          >
            <motion.div
               animate={{
                 scale: status === "speaking" ? [1, 1.03, 1] : [1, 1.01, 1],
               }}
               transition={{
                 duration: status === "speaking" ? 0.2 : 5,
                 repeat: Infinity,
                 ease: "easeInOut",
               }}
               className="w-full h-full"
            >
              <img 
                src={getImagePath()} 
                alt="Rose AI Persona"
                className="w-full h-full object-cover grayscale-[20%] brightness-[90%]"
              />
            </motion.div>
          </motion.div>
        </AnimatePresence>

        {/* Dynamic Speech Glow Overlay */}
        <AnimatePresence>
          {isActive && (
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ 
                opacity: status === "speaking" ? [0.1, 0.3, 0.1] : 0.1 
              }}
              transition={{ duration: 0.2, repeat: Infinity }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 bg-cyan-400/20 mix-blend-overlay"
            />
          )}
        </AnimatePresence>
      </div>

      {/* Scanning Ring */}
      <div className="absolute -inset-4 border border-cyan-500/20 rounded-full animate-[spin_20s_linear_infinite]" />
    </div>
  );
}


