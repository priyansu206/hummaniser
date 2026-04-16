from fastapi import FastAPI, Request
from groq import Groq
import os

app = FastAPI()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
@app.post("/api/humanize")
async def humanize_text(request: Request):
    data = await request.json()
    ai_text = data.get("text", "")
    system_prompt = """You are an expert human copywriter. Your task is to rewrite the provided AI-generated text to make it sound completely human. 
    Rules:
    - Drastically vary sentence length (burstiness).
    - Replace common AI buzzwords like 'delve', 'testament', or 'tapestry' with conversational alternatives (perplexity).
    - Introduce slight, natural imperfections.
    - Adopt a conversational tone. Do not output anything other than the rewritten text."""
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": ai_text}
        ],
        model="llama-3.3-70b-versatile", 
    )
    return {"humanized_text": chat_completion.choices[0].message.content}