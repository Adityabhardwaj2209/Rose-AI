"use client";

import { motion } from "framer-motion";
import { Lock, ShieldAlert, Cpu } from "lucide-react";

export default function LockedScreen({ onVerify }: { onVerify: () => void }) {
  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="fixed inset-0 z-[2000] bg-black/90 backdrop-blur-3xl flex items-center justify-center p-8 overflow-hidden"
    >
      {/* Glitch Overlay */}
      <div className="absolute inset-0 opacity-10 pointer-events-none">
        <div className="scanline" />
      </div>

      <div className="max-w-md w-full flex flex-col items-center gap-12 text-center relative">
        {/* Glow behind the lock */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-red-500/20 rounded-full blur-[100px]" />
        
        <motion.div 
          animate={{ rotate: [0, -5, 5, 0], scale: [1, 1.1, 1] }}
          transition={{ duration: 0.2, repeat: Infinity, repeatDelay: 5 }}
          className="p-8 glass-dark border border-red-500/30 rounded-full relative shadow-[0_0_50px_rgba(239,68,68,0.2)]"
        >
          <Lock className="w-16 h-16 text-red-500" />
          <div className="absolute -top-2 -right-2">
             <ShieldAlert className="w-8 h-8 text-red-400 animate-bounce" />
          </div>
        </motion.div>

        <div className="flex flex-col gap-4">
          <h1 className="text-3xl font-black tracking-[0.4em] text-white">NEURAL <span className="text-red-500">LOCKED</span></h1>
          <p className="text-sm text-white/40 uppercase tracking-[0.2em] leading-relaxed">Identity Mismatch Detected.<br/>Continuous Verification Failed.</p>
        </div>

        <div className="w-full flex flex-col gap-4">
            <button 
              onClick={onVerify}
              className="w-full p-4 glass border border-white/10 rounded-2xl text-white font-bold tracking-widest hover:bg-white/5 transition-all flex items-center justify-center gap-3"
            >
              <Cpu className="w-4 h-4 text-cyan-400" />
              IDENTIFY YOURSELF
            </button>
            <p className="text-[10px] text-white/20 uppercase tracking-[0.5em]">Voice Pattern Scan Pending</p>
        </div>
      </div>
    </motion.div>
  );
}
