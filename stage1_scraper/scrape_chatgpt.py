import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

PROMPTS_FILE = 'prompts.txt'
OUTPUT_FILE = 'output/brand_mentions.csv'
BRANDS = ['Nike', 'Adidas', 'Hoka', 'New Balance', 'Jordan']
CHATGPT_URL = 'https://chat.openai.com/'

# Helper to count brand mentions (case-insensitive, whole word)
def count_brands(text, brands):
    import re
    counts = {}
    for brand in brands:
        # Use word boundaries for whole word match, case-insensitive
        pattern = r'\\b' + re.escape(brand) + r'\\b'
        counts[brand] = len(re.findall(pattern, text, re.IGNORECASE))
    return counts

def main():
    # Read prompts
    with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
        prompts = [line.strip() for line in f if line.strip()]

    # Set up Selenium (Chrome)
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(CHATGPT_URL)

    print("Please log in to ChatGPT in the opened browser window. Press Enter here when ready...")
    input()

    results = []
    for idx, prompt in enumerate(prompts):
        print(f"[{idx+1}/{len(prompts)}] Sending prompt: {prompt}")
        # Find the textarea (prompt input)
        textarea = None
        for _ in range(10):
            try:
                textarea = driver.find_element(By.TAG_NAME, 'textarea')
                break
            except:
                time.sleep(1)
        if not textarea:
            print("Could not find prompt input box. Exiting.")
            driver.quit()
            return
        # Clear and send prompt
        textarea.clear()
        textarea.send_keys(prompt)
        textarea.send_keys(Keys.ENTER)

        last_response = ''
        for _ in range(60): 
            try:
                # Get all message blocks (ChatGPT responses)
                messages = driver.find_elements(By.CSS_SELECTOR, '[data-message-author-role="assistant"]')
                if messages:
                    last_response = messages[-1].text
                regen = driver.find_elements(By.XPATH, "//*[contains(text(), 'Regenerate') or contains(text(), 'Stop generating')]")
                if not regen:
                    break
            except:
                pass
            time.sleep(2)
        else:
            print("Timeout waiting for response.")

        # Count brand mentions
        counts = count_brands(last_response, BRANDS)
        row = {'prompt': prompt, **counts}
        results.append(row)
        print(f"Response: {counts}")
        time.sleep(3) 

    # Save to CSV
    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Results saved to {OUTPUT_FILE}")
    driver.quit()

if __name__ == '__main__':
    main() 