"use client";

import { motion } from "framer-motion";
import { Globe, Shield, Radio, Activity, Terminal } from "lucide-react";
import AirMap from "./AirMap";
import Analytics from "./Analytics";

export default function MissionHUD() {
  return (
    <div className="w-full h-full p-8 overflow-y-auto bg-[#020617] scroll-smooth custom-scroll">
      <div className="max-w-[1600px] mx-auto flex flex-col gap-8">
        
        {/* Header HUD */}
        <div className="flex justify-between items-end border-b border-white/5 pb-8">
          <div>
            <h1 className="text-4xl font-bold tracking-[0.4em] text-white">MISSION CONTROL <span className="text-cyan-400">UNIFIED</span></h1>
            <p className="text-xs text-cyan-400/50 uppercase tracking-[0.6em] mt-2">Neural Link: ACTIVE | System: SECURE</p>
          </div>
          <div className="flex gap-12">
            <HudStat label="Sky Status" value="CLEAR" icon={Radio} color="text-cyan-400" />
            <HudStat label="Orbital Link" value="SYNCED" icon={Globe} color="text-purple-400" />
            <HudStat label="Neural Guardian" value="ONLINE" icon={Shield} color="text-green-400" />
          </div>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-12 gap-8">
          {/* Tactical Radar Map */}
          <div className="col-span-12 xl:col-span-8 flex flex-col gap-4">
            <h2 className="text-sm font-bold uppercase tracking-widest text-white/40 flex items-center gap-2">
              <div className="w-1 h-1 rounded-full bg-cyan-400 animate-pulse" />
              Airspace & Orbital Scan
            </h2>
            <AirMap />
          </div>

          {/* System Logs / Neural Matrix */}
          <div className="col-span-12 xl:col-span-4 flex flex-col gap-4">
            <h2 className="text-sm font-bold uppercase tracking-widest text-white/40 flex items-center gap-2">
               <Terminal className="w-4 h-4" />
               Live Neural Matrix
            </h2>
            <div className="glass h-[400px] rounded-3xl border border-white/5 p-6 font-mono text-[10px] text-cyan-400/80 flex flex-col gap-2 overflow-y-auto no-scrollbar">
              <LogLine msg="Initializing High-Altitude Radar..." />
              <LogLine msg="Fetching TLE Data from CelesTrak..." />
              <LogLine msg="Neural Guardian: Outbound traffic scanned." />
              <LogLine msg="Tracking ISS (ZARYA) - Current Vector: North East" />
              <LogLine msg="Scam Shield: 12 risky nodes blocked." />
              <LogLine msg="Autonomous Mode: ACTIVE" />
            </div>
          </div>
        </div>

        {/* Analytics Layer */}
        <div className="flex flex-col gap-4">
          <h2 className="text-sm font-bold uppercase tracking-widest text-white/40">Life Analytics & Vitality</h2>
          <Analytics />
        </div>
      </div>
    </div>
  );
}

function HudStat({ label, value, icon: Icon, color }: any) {
  return (
    <div className="flex flex-col items-end gap-1">
      <div className="flex items-center gap-2">
        <Icon className={`w-4 h-4 ${color}`} />
        <span className="text-[10px] uppercase font-bold tracking-widest text-white/40">{label}</span>
      </div>
      <span className="text-xl font-mono text-white tracking-widest leading-none">{value}</span>
    </div>
  );
}

function LogLine({ msg }: any) {
  const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  return (
    <div className="flex gap-4">
      <span className="text-white/20">[{time}]</span>
      <span>{msg}</span>
    </div>
  );
}
