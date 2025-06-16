# Stage 2: Mentions API

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure you have run Stage 1 and have `brand_mentions.csv` in `../stage1_scraper/`.

3. Start the API server:
   ```bash
   uvicorn main:app --reload
   ```

4. Visit [http://127.0.0.1:8000/mentions](http://127.0.0.1:8000/mentions) in your browser or use curl/Postman.

## Endpoints

- `GET /mentions` – Returns total mentions for each brand (across all prompts)
- `GET /mentions/{brand}` – Returns total mentions for a specific brand (e.g., `/mentions/Nike`)

## Example Output

### `GET /mentions`
```json
{
  "Nike": 7,
  "Adidas": 5,
  "Hoka": 2,
  "New Balance": 3,
  "Jordan": 1
}
```

### `GET /mentions/Nike`
```json
{
  "Nike": 7
}
```

## Notes
- The database is automatically created from the CSV on first run.
- Edit `main.py` if you want to change the brands or CSV location. 