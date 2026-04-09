class ScenarioSimulator:
    def __init__(self, llm=None):
        self.llm = llm

    async def simulate_outcome(self, task: str):
        if not self.llm:
            return "Simulation engine disconnected (No LLM)."
        
        prompt = (
            f"Simulate the potential outcomes for the following task: '{task}'. "
            "Provide three scenarios: BEST CASE, WORST CASE, and MOST LIKELY. "
            "Be concise and focus on risks and benefits. Use casual Rose-AI tone."
        )
        
        try:
            resp = await self.llm.ainvoke(prompt)
            return resp.content
        except Exception as e:
            return f"Simulation Error: {e}"

scenario_simulator = ScenarioSimulator()
