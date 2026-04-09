"use client";

import { motion } from "framer-motion";
import { Activity, TrendingUp, DollarSign, Zap } from "lucide-react";

export default function Analytics() {
  const stats = [
    { label: "Productivity", value: "84%", icon: Zap, color: "text-yellow-400" },
    { label: "Focus Hours", value: "6.2h", icon: Activity, color: "text-cyan-400" },
    { label: "Daily Spend", value: "$12.40", icon: DollarSign, color: "text-green-400" },
    { label: "Burnout Risk", value: "Low", icon: TrendingUp, color: "text-purple-400" },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 w-full max-w-5xl mx-auto px-4 mt-8">
      {stats.map((stat, i) => (
        <motion.div
          key={stat.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.1 }}
          className="glass p-6 rounded-2xl border border-white/5 flex flex-col gap-2 relative group overflow-hidden"
        >
          <div className={`absolute inset-0 bg-gradient-to-br from-transparent to-white/5 opacity-0 group-hover:opacity-100 transition-opacity`} />
          <div className="flex items-center justify-between">
            <span className="text-[10px] uppercase tracking-[0.2em] text-white/40">{stat.label}</span>
            <stat.icon className={`w-4 h-4 ${stat.color} opacity-80`} />
          </div>
          <div className="text-2xl font-bold text-white tracking-tight">{stat.value}</div>
          
          {/* Sparkline Mockup */}
          <div className="mt-4 h-8 w-full flex items-end gap-1">
             {[0.4, 0.7, 0.5, 0.9, 0.6, 0.8, 1].map((h, j) => (
               <motion.div 
                 key={j}
                 initial={{ height: 0 }}
                 animate={{ height: `${h * 100}%` }}
                 transition={{ delay: 0.5 + (j * 0.05) }}
                 className={`flex-1 rounded-t-sm ${stat.color} opacity-30`}
               />
             ))}
          </div>
        </motion.div>
      ))}
    </div>
  );
}
