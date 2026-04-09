import networkx as nx
import os
import json

class KnowledgeGraph:
    def __init__(self):
        self.graph_path = "data/memory/knowledge_graph.json"
        os.makedirs("data/memory", exist_ok=True)
        self.G = nx.Graph()
        self._load_graph()

    def _load_graph(self):
        if os.path.exists(self.graph_path):
            with open(self.graph_path, 'r') as f:
                data = json.load(f)
                for node in data.get("nodes", []):
                    self.G.add_node(node["id"], **node.get("data", {}))
                for edge in data.get("edges", []):
                    self.G.add_edge(edge["source"], edge["target"], **edge.get("data", {}))
        else:
            # Seed the graph with core concepts
            self.G.add_node("User", label="Person")
            self.G.add_node("Rose", label="AI Entity")
            self.G.add_edge("User", "Rose", relation="Collaborating")

    def add_connection(self, source, target, relation="Relative"):
        self.G.add_node(source)
        self.G.add_node(target)
        self.G.add_edge(source, target, relation=relation)
        self._save_graph()

    def scan_workspace(self, root_dir: str):
        """Builds knowledge from local files."""
        count = 0
        for root, dirs, files in os.walk(root_dir):
            if ".git" in root or "node_modules" in root: continue
            for file in files:
                if file.endswith((".py", ".tsx", ".md", ".json")):
                    self.add_connection("User", file, relation="Authoring")
                    count += 1
        return f"Neural Scan: Indexed {count} work entities into the Knowledge Graph."

    def _save_graph(self):
        nodes = [{"id": n, "data": self.G.nodes[n]} for n in self.G.nodes()]
        edges = [{"source": u, "target": v, "data": self.G.edges[u, v]} for u, v in self.G.edges()]
        with open(self.graph_path, 'w') as f:
            json.dump({"nodes": nodes, "edges": edges}, f, indent=4)

knowledge_graph = KnowledgeGraph()
