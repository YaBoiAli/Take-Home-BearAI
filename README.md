# Bear AI Technical Take-Home Assignment

This project consists of two stages:
1. Web scraping ChatGPT responses for brand mentions
2. Building an API to serve the brand mention metrics

## Stage 1: Web Scraping Setup

### Prerequisites
- Python 3.8 or higher
- Google Chrome browser
- A logged-in ChatGPT account

### Setup Instructions
1. Navigate to the `stage1_scraper` directory:
   ```bash
   cd stage1_scraper
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the `stage1_scraper` directory with your Chrome user data directory:
   ```
   CHROME_USER_DATA_DIR=C:\Users\YourUsername\AppData\Local\Google\Chrome\User Data
   ```
   Replace `YourUsername` with your Windows username.

4. Run the scraper:
   ```bash
   python chatgpt_scraper.py
   ```

The script will:
- Open Chrome with your logged-in profile
- Navigate to ChatGPT
- Send 10 different prompts about sportswear
- Count brand mentions in the responses
- Save results to `brand_mentions.json`

### Output Format
The script generates a JSON file with the following structure:
```json
[
  {
    "prompt": "What are the best running shoes in 2025?",
    "timestamp": "2024-03-14T12:00:00.000Z",
    "brand_mentions": {
      "Nike": 3,
      "Adidas": 2,
      "Hoka": 1,
      "New Balance": 2,
      "Jordan": 0
    }
  },
  // ... more results
]
```

## Stage 2: API Setup
(Coming soon)

## Example Output

## Suggestions for Improvements 