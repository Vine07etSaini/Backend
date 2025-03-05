from openai import OpenAI
from dotenv import load_dotenv
import os
async def expand_query(user_query: str)->list[str]:
      
      try:

        load_dotenv()
        client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv('DEEPSEEK_API_KEY'),
        )
        response=client.chat.completions.create(
          model="deepseek/deepseek-r1:free",
          messages=[{"role":"user","content":f"Generate 10 short search feasible query variants for: {user_query}. Return only the queries, separated by newlines"}]
        )

        return [choice.message.content.strip() for choice in response.choices]
      
      except Exception as e:
        print(f"[ERROR] Failed to Expand Query: {e}")
        return []
      