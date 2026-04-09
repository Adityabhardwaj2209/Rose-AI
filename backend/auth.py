import requests
import os
import hashlib
import json

class KeyAuth:
    def __init__(self, name, ownerid, sellerkey=None):
        self.name = name
        self.ownerid = ownerid
        self.sellerkey = sellerkey
        self.base_url = "https://keyauth.win/api/1.2/"

    def check_license(self, key):
        """Standard client-side license check."""
        # Note: In a real app, we would use the official KeyAuth library for HWID checks
        # For this implementation, we simulate the verification
        print(f"Verifying license key: {key}")
        return True # Mock success for development

    def create_license(self, expiry=30):
        """Seller-side license creation using KeyAuth API."""
        if not self.sellerkey:
            return {"error": "Seller Key not provided. JARVIS cannot generate licenses."}

        url = f"https://keyauth.win/api/seller/?sellerkey={self.sellerkey}&type=add&expiry={expiry}&mask=JARVIS-XXXXXX"
        try:
            response = requests.get(url)
            data = response.json()
            if data.get("success"):
                return {"key": data.get("key"), "message": "License generated successfully."}
            return {"error": data.get("message")}
        except Exception as e:
            return {"error": str(e)}

# Initialize auth with env vars
auth_engine = KeyAuth(
    name=os.getenv("KEYAUTH_NAME", "JARVIS"),
    ownerid=os.getenv("KEYAUTH_OWNERID", ""),
    sellerkey=os.getenv("KEYAUTH_SELLERKEY", "")
)
