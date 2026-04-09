import json
import os
from datetime import datetime

class SmartLedger:
    def __init__(self):
        self.ledger_path = "data/finance/ledger.json"
        os.makedirs("data/finance", exist_ok=True)
        self.ledger = self._load_ledger()

    def _load_ledger(self):
        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, 'r') as f:
                return json.load(f)
        return []

    def log_expense(self, merchant: str, amount: float, category: str = "Uncategorized"):
        """Logs a new expense to the ledger."""
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "merchant": merchant,
            "amount": amount,
            "category": category
        }
        self.ledger.append(entry)
        self._save_ledger()
        return f"Gotchu! Logged ${amount} at {merchant} under {category}."

    def _save_ledger(self):
        with open(self.ledger_path, 'w') as f:
            json.dump(self.ledger, f, indent=4)

    def get_summary(self):
        total = sum(item['amount'] for item in self.ledger)
        count = len(self.ledger)
        return f"Total spending: ${total:.2f} across {count} transactions."

smart_ledger = SmartLedger()
