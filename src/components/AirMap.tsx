"use client";

import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { Plane, AlertTriangle, Radio } from "lucide-react";
import { useEffect, useState } from "react";

// Fix for default marker icons in Leaflet + Next.js
const planeIcon = new L.DivIcon({
  html: `<div class="text-cyan-400 rotate-45"><svg xmlns="http://www.w3.org/1999/xlink" viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"></path></svg></div>`,
  className: "custom-div-icon",
  iconSize: [24, 24],
});

interface Aircraft {
  id: string;
  flight: string;
  lat: number;
  lon: number;
  altitude: number;
  speed: number;
  distance: number;
  risk: string;
}

export default function AirMap() {
  const [aircraft, setAircraft] = useState<Aircraft[]>([]);
  const [userPos, setUserPos] = useState<[number, number]>([28.6139, 77.2090]); // Default New Delhi

  useEffect(() => {
    // Polling Radar Data
    const fetchRadar = async () => {
      try {
        const resp = await fetch("http://localhost:8000/api/command", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: "INTERNAL_RADAR_QUERY" }),
        });
        const data = await resp.json();
        if (data.aircraft) setAircraft(data.aircraft);
      } catch (e) {
        console.error("Radar sync error:", e);
      }
    };

    fetchRadar();
    const interval = setInterval(fetchRadar, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full h-[400px] glass rounded-3xl border border-white/5 overflow-hidden relative group">
      <div className="absolute top-4 left-4 z-[400] flex items-center gap-2 bg-[#020617]/80 px-4 py-2 rounded-full border border-cyan-400/20 shadow-xl">
        <Radio className="w-4 h-4 text-cyan-400 animate-pulse" />
        <span className="text-[10px] uppercase font-bold tracking-[0.2em] text-cyan-400">Live Airspace Radar</span>
      </div>

      <MapContainer 
        center={userPos} 
        zoom={9} 
        scrollWheelZoom={false}
        className="w-full h-full grayscale invert opacity-80 brightness-75 contrast-125"
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {aircraft.map((ac) => (
          <Marker 
            key={ac.id} 
            position={[ac.lat, ac.lon]} 
            icon={planeIcon}
          >
            <Popup className="tactical-popup">
              <div className="bg-[#020617] text-white p-2 rounded-lg border border-cyan-400/30">
                <p className="text-cyan-400 font-bold tracking-widest">{ac.flight}</p>
                <p className="text-[10px] text-white/60 uppercase mt-1">ALT: {ac.altitude} FT</p>
                <p className="text-[10px] text-white/60 uppercase">SPD: {ac.speed} KT</p>
                {ac.risk !== "NORMAL" && (
                   <p className="text-[10px] text-red-400 font-bold uppercase mt-1 flex items-center gap-1">
                     <AlertTriangle className="w-3 h-3" /> {ac.risk.replace("_", " ")}
                   </p>
                )}
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
