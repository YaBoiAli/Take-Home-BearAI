import os
import asyncio
import csv
import random
from datetime import datetime
from pyppeteer import launch
from dotenv import load_dotenv

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

    async def setup_browser(self):
        chrome_path = os.getenv('CHROME_EXECUTABLE_PATH')
        if not chrome_path or not os.path.exists(chrome_path):
            print("Could not find Chrome executable path in .env or the path is invalid.")
            print("Please enter the full path to your chrome.exe (e.g., C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe):")
            chrome_path = input().strip()
            if not os.path.exists(chrome_path):
                raise ValueError(f"Chrome executable not found at {chrome_path}")
            with open('.env', 'a') as f:
                f.write(f"\nCHROME_EXECUTABLE_PATH={chrome_path}")
        print(f"Launching Chrome from: {chrome_path}")
        browser = await launch({
            'headless': False,
            'executablePath': chrome_path,
            'args': [
                '--window-size=1920,1080',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-site-isolation-trials',
                '--no-sandbox'
            ],
            'ignoreDefaultArgs': ['--enable-automation'],
            'handleSIGINT': False,
            'handleSIGTERM': False,
            'handleSIGHUP': False
        })
        return browser

    async def robust_type(self, page, selector, text, prompt_idx=0):
        await page.evaluate(f'''
            (selector) => {{
                const el = document.querySelector(selector);
                if (el) el.scrollIntoView({{behavior: 'smooth', block: 'center'}});
            }}
        ''', selector)
        await asyncio.sleep(0.5)
        await page.focus(selector)
        await asyncio.sleep(0.2)
        try:
            await page.type(selector, text, {'delay': random.randint(50, 150)})
        except Exception as e:
            print(f"page.type() failed, trying JS injection: {e}")
            # Set innerText directly and dispatch input event
            await page.evaluate(f'''
                (selector, value) => {{
                    const el = document.querySelector(selector);
                    el.innerText = value;
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            ''', selector, text)
        await asyncio.sleep(0.5)

    async def random_scroll(self, page):
        await page.evaluate(f'''
            window.scrollBy(0, {random.randint(100, 300)});
        ''')
        await asyncio.sleep(random.uniform(0.5, 1.5))

    def count_brand_mentions(self, text):
        counts = {brand: text.lower().count(brand.lower()) for brand in self.brands}
        return counts

    async def scrape_responses(self):
        browser = await self.setup_browser()
        page = await browser.newPage()
        try:
            await page.setViewport({'width': 1920, 'height': 1080})
            await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
            print("Navigating to ChatGPT...")
            await page.goto('https://chat.openai.com/')
            await asyncio.sleep(5)
            print("Please log in to ChatGPT in the opened browser, then press Enter here to continue...")
            input()
            for idx, prompt in enumerate(self.prompts):
                print(f"Processing prompt: {prompt}")
                await self.random_scroll(page)
                selector = '#prompt-textarea'
                print(f"Waiting for input box with selector: {selector}")
                await page.waitForSelector(selector, {'timeout': 20000})
                print("Input box found, typing prompt...")
                await self.robust_type(page, selector, prompt, idx)
                print("Prompt typed.")
                await asyncio.sleep(random.uniform(0.5, 1.5))
                await page.keyboard.press('Enter')
                print("Prompt sent. Waiting for response...")
                await asyncio.sleep(random.uniform(8, 12))
                await self.random_scroll(page)
                response_elements = await page.querySelectorAll('div.markdown')
                response_text = ' '.join([await page.evaluate('(element) => element.textContent', element) for element in response_elements])
                brand_counts = self.count_brand_mentions(response_text)
                result = {
                    "prompt": prompt,
                    "timestamp": datetime.now().isoformat(),
                    **brand_counts
                }
                self.results.append(result)
                self.save_results_csv()
                await asyncio.sleep(random.uniform(2, 4))
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            await browser.close()

    def save_results_csv(self):
        fieldnames = ["prompt", "timestamp"] + self.brands
        with open('brand_mentions.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.results:
                writer.writerow(row)

async def main():
    scraper = ChatGPTScraper()
    await scraper.scrape_responses()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main()) 