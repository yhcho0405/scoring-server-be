import numpy as np
import torch
from torch.nn import functional as F
from transformers import BertModel, BertTokenizer
from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

model_name = "kykim/bert-kor-base"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

app = FastAPI()

class SimilarityRequest(BaseModel):
    sentence1: str
    sentence2: str

async def get_embedding(text):
    tokens = tokenizer.tokenize(text)
    print(f"Tokens for '{text}': {tokens}")

    token_ids = tokenizer.encode(text, add_special_tokens=True)
    print(f"Token IDs for '{text}': {token_ids}")

    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    
    loop = asyncio.get_event_loop()
    outputs = await loop.run_in_executor(None, lambda: model(**inputs))
    
    # [CLS] token
    return outputs.last_hidden_state[:, 0, :].squeeze().detach().numpy()

@app.post("/api/similarity")
async def calculate_similarity(request: SimilarityRequest):
    embedding1, embedding2 = await asyncio.gather(
        get_embedding(request.sentence1),
        get_embedding(request.sentence2)
    )
    
    similarity = F.cosine_similarity(torch.tensor(embedding1).unsqueeze(0), 
                                     torch.tensor(embedding2).unsqueeze(0)).item()
    percentage = (similarity + 1) / 2 * 100
    
    return {"result": round(percentage, 2)}

@app.post("/api/similarity/score")
async def calculate_similarity_score(request: SimilarityRequest):
    embedding1, embedding2 = await asyncio.gather(
        get_embedding(request.sentence1),
        get_embedding(request.sentence2)
    )
    
    similarity = F.cosine_similarity(torch.tensor(embedding1).unsqueeze(0), 
                                     torch.tensor(embedding2).unsqueeze(0)).item()
    percentage = (similarity + 1) / 2 * 100

    base = 1.2
    score = (base ** percentage - 1) / (base ** 100 - 1) * 100
    
    return {"result": round(score, 2)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)