import os
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ChatGPTScraper:
    def __init__(self):
        self.brands = ['Nike', 'Adidas', 'Hoka', 'New Balance', 'Jordan']
        self.prompts = [
            "What are the best running shoes in 2025?",
            "Top performance sneakers for athletes",
            "Most comfortable athletic shoes for daily wear",
            "Best basketball shoes for professional players",
            "Top-rated cross-training shoes",
            "Most popular athletic footwear brands",
            "Best shoes for marathon runners",
            "Top-rated tennis shoes",
            "Most innovative sports shoe technologies",
            "Best shoes for high-impact sports"
        ]
        self.results = []
        
    def setup_driver(self):
        """Set up Chrome driver with user profile"""
        chrome_options = Options()
        
        # Get the user's Chrome profile directory
        user_data_dir = os.getenv('CHROME_USER_DATA_DIR')
        if not user_data_dir:
            raise ValueError("Please set CHROME_USER_DATA_DIR in .env file")
            
        chrome_options.add_argument(f"user-data-dir={user_data_dir}")
        chrome_options.add_argument("--profile-directory=Default")
        
        # Initialize the Chrome driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def count_brand_mentions(self, text):
        """Count mentions of each brand in the text"""
        counts = {brand: text.lower().count(brand.lower()) for brand in self.brands}
        return counts

    def scrape_responses(self):
        """Main function to scrape ChatGPT responses"""
        driver = self.setup_driver()
        
        try:
            # Navigate to ChatGPT
            driver.get("https://chat.openai.com/")
            time.sleep(5)  # Wait for page to load
            
            for prompt in self.prompts:
                print(f"Processing prompt: {prompt}")
                
                # Find and fill the input box
                input_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[data-id='root']"))
                )
                input_box.clear()
                input_box.send_keys(prompt)
                input_box.submit()
                
                # Wait for response
                time.sleep(10)  # Adjust based on response time
                
                # Get the response text
                response_elements = driver.find_elements(By.CSS_SELECTOR, "div.markdown")
                response_text = " ".join([elem.text for elem in response_elements])
                
                # Count brand mentions
                brand_counts = self.count_brand_mentions(response_text)
                
                # Store results
                result = {
                    "prompt": prompt,
                    "timestamp": datetime.now().isoformat(),
                    "brand_mentions": brand_counts
                }
                self.results.append(result)
                
                # Save results after each prompt
                self.save_results()
                
                time.sleep(2)  # Brief pause between prompts
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            driver.quit()

    def save_results(self):
        """Save results to JSON file"""
        with open('brand_mentions.json', 'w') as f:
            json.dump(self.results, f, indent=2)

if __name__ == "__main__":
    scraper = ChatGPTScraper()
    scraper.scrape_responses() 