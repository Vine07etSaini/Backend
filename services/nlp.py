from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model=SentenceTransformer('all-MiniLM-L6-v2')


def rank_results(query: str , results: list):
    query_embedding = model.encode(query)
    for result in results:
        if not isinstance(result, dict) or 'snippet' not in result:
            continue
        result_embedding = model.encode(result['snippet'])
        similarity = cosine_similarity(
            [query_embedding], 
            [result_embedding]
        )[0][0]
        
        # Convert numpy.float32 to Python float
        result["relevance"] = float(similarity) 
    return sorted(results, key=lambda x: x.get("relevance", 0), reverse=True)