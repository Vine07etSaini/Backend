import httpx


def parse_youtube_results(youtube_data: dict) -> list:
    """Parse YouTube Data API response."""
    results = []
    if "items" not in youtube_data:
        return results
    
    for item in youtube_data["items"]:
        snippet = item.get("snippet", {})
        results.append({
            "title": snippet.get("title", ""),
            "link": f"https://youtu.be/{item['id']['videoId']}",
            "snippet": snippet.get("description", ""),
            "source": "youtube"
        })
    return results

async def search_youtube(query:str , api_key:str):
    async with httpx.AsyncClient() as client:
        try:
                response = await client.get(
                "https://www.googleapis.com/youtube/v3/search",
                 params={
                 "key":api_key,
                 "part":"snippet",
                 "q":query,
                 "maxResult":20
                 } )
                response.raise_for_status()
                return parse_youtube_results(response.json())
            
        except Exception as e:
            print(f"YouTube API Error: {e}")
            return []


