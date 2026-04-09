from skyfield.api import Topos, load
import os
import pandas as pd
from datetime import datetime, timedelta

class CosmicRadar:
    def __init__(self):
        self.stations_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle'
        self.sat_data_path = "data/cosmic/satellites.tle"
        os.makedirs("data/cosmic", exist_ok=True)
        self.ts = load.timescale()
        self.stations = self._load_stations()

    def _load_stations(self):
        """Downloads and loads TLE data for major stations (ISS, etc)."""
        try:
            stations = load.tle_file(self.stations_url)
            return {sat.name: sat for sat in stations}
        except Exception as e:
            print(f"Cosmic Sync Error: {e}")
            return {}

    def get_iss_position(self, user_lat=28.6139, user_lon=77.2090):
        """Calculates the current ISS position relative to the user."""
        if 'ISS (ZARYA)' not in self.stations:
            return "ISS Data unavailable."
        
        iss = self.stations['ISS (ZARYA)']
        t = self.ts.now()
        geocentric = iss.at(t)
        subpoint = geocentric.subpoint()
        
        # Calculate when it will pass over
        site = Topos(user_lat, user_lon)
        t0 = self.ts.now()
        t1 = self.ts.from_datetimes([datetime.now() + timedelta(hours=24)])
        # Find passes
        # times, events = iss.find_events(site, t0, t1, altitude_degrees=30.0)
        
        return {
            "name": "ISS",
            "lat": subpoint.latitude.degrees,
            "lon": subpoint.longitude.degrees,
            "alt_km": subpoint.elevation.km,
            "summary": f"ISS is currently at {subpoint.latitude.degrees:.2f}, {subpoint.longitude.degrees:.2f}."
        }

cosmic_radar = CosmicRadar()
