from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from services.query import expand_query  
from services.google import search_google
from services.youtube import search_youtube
from services.nlp import rank_results
import asyncio
import os
import re

load_dotenv()
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],)

@app.get("/health")
async def health_check():
    return {"status":"Ok"}

@app.get("/env-test")
async def env_test():
    return {
        "deepseek_key": os.getenv("DEEPSEEK_API_KEY")[:4] + "..." if os.getenv("DEEPSEEK_API_KEY") else None
    }

@app.post("/search")
async def search(query: str):
    try:
        # Step 1: Query expansion
        queries = await expand_query(query)
        # Step 2: Concurrent API calls
        google_results, youtube_results = await asyncio.gather(
            search_google(queries[0], os.getenv("GOOGLE_API_KEY"), os.getenv("GOOGLE_CX")),
            search_youtube(queries[0], os.getenv("YOUTUBE_API_KEY"))
        )
        
        google_results=rank_results(query,google_results)
        youtube_results=rank_results(query,youtube_results)
        return {
            "query": query,
            "results": {
                "google": google_results,
                "youtube": youtube_results
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))