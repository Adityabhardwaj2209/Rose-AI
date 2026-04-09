"use client";

import { motion } from "framer-motion";

interface OrbProps {
  status?: "idle" | "thinking" | "speaking" | "listening";
}

export default function TheOrb({ status = "idle" }: OrbProps) {
  const getColors = () => {
    switch (status) {
      case "thinking":
        return ["#a855f7", "#ec4899", "#a855f7"];
      case "listening":
        return ["#22d3ee", "#00d4ff", "#22d3ee"];
      case "speaking":
        return ["#22d3ee", "#a855f7", "#22d3ee"];
      default:
        return ["#22d3ee99", "#22d3ee33", "#22d3ee99"];
    }
  };

  return (
    <div className="relative flex items-center justify-center w-64 h-64">
      {/* Outer Glow */}
      <motion.div
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.3, 0.6, 0.3],
        }}
        transition={{
          duration: 4,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute w-full h-full rounded-full blur-3xl"
        style={{
          background: `radial-gradient(circle, ${getColors()[0]}, transparent)`,
        }}
      />

      {/* Main Orb Body */}
      <motion.div
        animate={{
          scale: status === "thinking" ? [1, 1.1, 1] : status === "listening" ? [1, 1.05, 1] : 1,
          rotate: 360,
        }}
        transition={{
          scale: { duration: 2, repeat: Infinity },
          rotate: { duration: 20, repeat: Infinity, ease: "linear" },
        }}
        className="relative w-48 h-48 rounded-full border border-cyan-400/30 glass flex items-center justify-center overflow-hidden"
      >
        {/* Internal Core */}
        <motion.div
          animate={{
            scale: [0.8, 1, 0.8],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="w-24 h-24 rounded-full"
          style={{
            background: `radial-gradient(circle, ${getColors()[1]} 0%, transparent 70%)`,
            boxShadow: `0 0 30px ${getColors()[1]}`,
          }}
        />

        {/* Floating Particles/Lines (Decorative) */}
        <div className="absolute inset-0 opacity-20">
          {[...Array(3)].map((_, i) => (
            <motion.div
              key={i}
              animate={{
                rotate: 360,
              }}
              transition={{
                duration: 10 + i * 5,
                repeat: Infinity,
                ease: "linear",
              }}
              className="absolute inset-0 border border-dashed border-cyan-500 rounded-full"
              style={{ margin: `${i * 20}px` }}
            />
          ))}
        </div>
      </motion.div>

      {/* Scanning Rings */}
      {status === "listening" && (
        <motion.div
          animate={{
            scale: [1, 2],
            opacity: [1, 0],
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            ease: "easeOut",
          }}
          className="absolute w-48 h-48 rounded-full border-2 border-cyan-400"
        />
      )}
    </div>
  );
}
