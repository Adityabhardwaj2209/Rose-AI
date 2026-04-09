class RiskEngine:
    def __init__(self):
        self.risk_score = 0
        self.last_check = time.time()
        # Sensitivity Tiers: 1=Safe, 2=Cautious, 3=Strict
        self.action_matrix = {
            "iot": 1,
            "radar": 1,
            "weather": 1,
            "email": 2,
            "calendar": 2,
            "finance": 3,
            "security": 3,
            "system": 3
        }

    def get_permissibility(self, tool_name: str, context: dict):
        """
        Determines the Autonomy Level for a specific tool.
        Returns: 'FULL', 'CONFIRMED', '2FA', or 'BLOCKED'
        """
        base_risk = self.calculate_risk(context)
        tool_sensitivity = self.action_matrix.get(tool_name, 2)

        # Unknown Network Escalation (The Coffee-Shop Rule)
        if context.get("network") == "unknown":
            return "2FA" if tool_sensitivity >= 2 else "CONFIRMED"

        if base_risk < 20: return "FULL"
        if base_risk < 50: return "CONFIRMED"
        return "2FA"

    def calculate_risk(self, context: dict):
        # ... logic ...

risk_engine = RiskEngine()
