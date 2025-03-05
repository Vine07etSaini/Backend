import httpx

def parse_google_results(google_data: dict) -> list:
    """Parse Google Custom Search JSON response."""
    results = []
    try:
        if "items" not in google_data:
            print(f"[WARN] No 'items' in Google response: {google_data}")
            return results
        
        for item in google_data["items"]:
            results.append({
                "title": item.get("title", "No title"),
                "link": item.get("link", "#"),
                "snippet": item.get("snippet", "No description"),
                "source": "google"
            })
        return results
    except Exception as e:
        print(f"[ERROR] Failed to parse Google results: {e}")
        return []

async def search_google(query:str,api_key:str,cx:str):
    async with httpx.AsyncClient() as client:
       response= await client.get(
          "https://www.googleapis.com/customsearch/v1",
          params={"key":api_key ,"cx":cx ,"q":query}
       )
       return parse_google_results(response.json())
