from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import urllib.request
import urllib.error
import json
import os
app = FastAPI()
class TextInput(BaseModel):
    text: str
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Humanizer</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; }
        textarea { width: 100%; height: 150px; margin-bottom: 10px; padding: 10px; }
        button { padding: 10px 20px; cursor: pointer; background: #000; color: #fff; border: none; }
        #output { margin-top: 20px; padding: 15px; background: #f4f4f4; border-radius: 5px; min-height: 50px; white-space: pre-wrap;}
    </style>
</head>
<body>
    <h2>AI Text Humanizer</h2>
    <p>Paste your robotic AI text below:</p>
    
    <textarea id="inputText" placeholder="Enter text here..."></textarea>
    <button onclick="humanize()">Humanize Text</button>

    <div id="output">Your humanized text will appear here...</div>

    <script>
        async function humanize() {
            const text = document.getElementById('inputText').value;
            const outputDiv = document.getElementById('output');
            outputDiv.innerText = "Thinking...";

            try {
                const response = await fetch('/humanize', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });

                const data = await response.json();
                outputDiv.innerText = data.humanized_text || "An error occurred.";
            } catch (err) {
                outputDiv.innerText = "Error: Connection error.";
            }
        }
    </script>
</body>
</html>
"""
@app.get("/")
def serve_home():
    return HTMLResponse(content=HTML_TEMPLATE)
@app.post("/humanize")
def humanize_text(data: TextInput):
    api_key = os.environ.get("GROQ_API_KEY", "").strip() 
    if not api_key:
        return {"humanized_text": "Error: Vercel cannot find the GROQ_API_KEY. Did you add it to Vercel Environment Variables?"}
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" # <-- ADD THIS LINE
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert human copywriter. Your task is to rewrite the provided AI-generated text to make it sound completely human. Rules: - Drastically vary sentence length (burstiness). - Replace common AI buzzwords like 'delve', 'testament', or 'tapestry' with conversational alternatives. - Introduce slight, natural imperfections. - Adopt a conversational tone. Do not output anything other than the rewritten text."
            },
            {
                "role": "user",
                "content": data.text
            }
        ]
    }
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            return {"humanized_text": result["choices"][0]["message"]["content"]}           
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return {"humanized_text": f"HTTP Error {e.code}: {error_body}"}
    except Exception as e:
        return {"humanized_text": f"Raw Network Error: {repr(e)}"}