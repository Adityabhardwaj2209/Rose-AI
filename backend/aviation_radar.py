import requests
import geocoder
from geopy.distance import geodesic
import time

class AviationRadar:
    def __init__(self):
        self.base_url = "https://api.adsb.lol/v2/lat/{lat}/lon/{lon}/dist/{dist}"
        self.alerts_log = []

    def get_nearby_aircraft(self, radius_miles: int = 20):
        """Fetches live aircraft data within a specific distance."""
        try:
            # 1. Get User Location
            g = geocoder.ip('me')
            lat, lon = g.latlng[0], g.latlng[1] if g.latlng else (40.7128, -74.0060)
            
            # 2. Poll ADS-B Data (ADSB.lol is a community unfiltered feed)
            # Distance converted to KM for the API
            url = self.base_url.format(lat=lat, lon=lon, dist=int(radius_miles * 1.609))
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                aircraft = data.get("ac", [])
                return self._process_aircraft(aircraft, lat, lon)
            return []
        except Exception as e:
            print(f"Radar Error: {e}")
            return []

    def _process_aircraft(self, aircraft_list, user_lat, user_lon):
        processed = []
        for ac in aircraft_list:
            # Calculate distance
            ac_lat, ac_lon = ac.get("lat"), ac.get("lon")
            dist = 0
            if ac_lat and ac_lon:
                dist = geodesic((user_lat, user_lon), (ac_lat, ac_lon)).miles

            processed.append({
                "id": ac.get("icao"),
                "flight": ac.get("flight", "UNK").strip(),
                "altitude": ac.get("alt_baro", 0),
                "speed": ac.get("gs", 0),
                "distance": round(dist, 1),
                "lat": ac_lat,
                "lon": ac_lon,
                "type": ac.get("t", "Aircraft"),
                "risk": self._analyze_risk(ac, dist)
            })
        return sorted(processed, key=lambda x: x['distance'])

    def _analyze_risk(self, ac, dist):
        alt = ac.get("alt_baro", 30000)
        if isinstance(alt, str): alt = 0 # Handle non-numeric alt
        
        if dist < 5 and alt < 5000:
            return "LOW_ALTITUDE_WARNING"
        if ac.get("squawk") == "7700":
            return "EMERGENCY_DETECTED"
        return "NORMAL"

aviation_radar = AviationRadar()
