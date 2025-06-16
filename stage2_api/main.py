"""
FastAPI app exposing endpoints to serve brand mention metrics from the database.
"""
import os
import sqlite3
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

DB_PATH = 'brand_mentions.db'
CSV_PATH = '../stage1_scraper/brand_mentions.csv'
BRANDS = ['Nike', 'Adidas', 'Hoka', 'New Balance', 'Jordan']

app = FastAPI()

def init_db():
    if not os.path.exists(DB_PATH):
        df = pd.read_csv(CSV_PATH)
        conn = sqlite3.connect(DB_PATH)
        df.to_sql('mentions', conn, index=False, if_exists='replace')
        conn.close()

@app.on_event('startup')
def startup_event():
    init_db()

@app.get('/mentions')
def get_mentions():
    conn = sqlite3.connect(DB_PATH)
    query = f"SELECT {', '.join([f'SUM([{b}]) as [{b}]' for b in BRANDS])} FROM mentions"
    row = conn.execute(query).fetchone()
    conn.close()
    return {brand: int(row[i]) for i, brand in enumerate(BRANDS)}

@app.get('/mentions/{brand}')
def get_brand_mentions(brand: str):
    if brand not in BRANDS:
        raise HTTPException(status_code=404, detail='Brand not found')
    conn = sqlite3.connect(DB_PATH)
    query = f"SELECT SUM([{brand}]) FROM mentions"
    row = conn.execute(query).fetchone()
    conn.close()
    return {brand: int(row[0])} 