from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class CareerAgent:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless") # Run in background
        self.chrome_options.add_argument("--disable-gpu")

    def search_jobs(self, role: str, location: str = "remote"):
        """Automates job searching via Google Jobs."""
        try:
            driver = webdriver.Chrome(options=self.chrome_options)
            search_url = f"https://www.google.com/search?q=jobs+for+{role}+in+{location}"
            driver.get(search_url)
            time.sleep(3)
            
            # Extract top job titles (Simplified for demo)
            results = driver.find_elements(By.CSS_SELECTOR, "div.BJWtP")
            job_list = []
            for res in results[:3]:
                job_list.append(res.text)
            
            driver.quit()
            
            if job_list:
                return f"Yo, I found some potential gigs for you: {', '.join(job_list)}. Want me to dig deeper into one?"
            return f"Man, it's a bit dry out there for {role} roles right now."
            
        except Exception as e:
            return f"Job search error: {e}"

career_agent = CareerAgent()
