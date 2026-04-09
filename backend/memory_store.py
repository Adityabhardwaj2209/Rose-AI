import chromadb
from chromadb.config import Settings
import time
import os

class MemoryStore:
    def __init__(self):
        self.persist_directory = "data/memory"
        os.makedirs(self.persist_directory, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection(name="jarvis_memory")

    def store_interaction(self, user_input: str, jarvis_output: str):
        """Stores a conversation pair for future context."""
        timestamp = time.time()
        self.collection.add(
            documents=[f"User: {user_input}\nJARVIS: {jarvis_output}"],
            metadatas=[{"timestamp": timestamp, "type": "conversation"}],
            ids=[f"conv_{int(timestamp)}"]
        )

    def learn_habit(self, interaction_type: str):
        """Tracks common patterns to learn user habits."""
        current_time = time.localtime()
        hour = current_time.tm_hour
        timestamp = time.strftime("%H:%M", current_time)
        
        self.collection.add(
            documents=[f"Interaction: {interaction_type} at {timestamp}"],
            metadatas=[{"timestamp": time.time(), "type": "habit", "hour": hour}],
            ids=[f"habit_{int(time.time() * 1000)}"]
        )

    def analyze_habits(self):
        """Analyzes stored data to find patterns (Point 13: Life Analytics)."""
        results = self.collection.get(where={"type": "habit"})
        if not results['metadatas']:
            return "Not enough data to find patterns yet, dude."
            
        hours = [m['hour'] for m in results['metadatas']]
        most_common_hour = max(set(hours), key=hours.count)
        
        return f"You're most active around {most_common_hour}:00. Shall we set that as focus mode?"

    def recall(self, query: str, limit: int = 3):
        """Recalls past interactions similar to the query."""
        results = self.collection.query(
            query_texts=[query],
            n_results=limit
        )
        return results['documents'][0] if results['documents'] else []

memory_store = MemoryStore()

