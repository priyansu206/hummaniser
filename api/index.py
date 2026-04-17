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
    <title>AI Humanizer | Neobrutalism</title>
    <style>
        :root {
            --bg-color: #fff4da; /* Retro warm cream */
            --border-color: #000000;
            --accent-purple: #c084fc;
            --accent-green: #4ade80;
            --accent-orange: #fb923c;
            --shadow: 6px 6px 0px var(--border-color);
            --shadow-pressed: 2px 2px 0px var(--border-color);
        }
        body {
            font-family: 'Courier New', Courier, monospace;
            background-color: var(--bg-color);
            background-image: radial-gradient(#000000 1px, transparent 1px);
            background-size: 20px 20px;
            color: #000;
            min-height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background-color: #ffffff;
            border: 4px solid var(--border-color);
            padding: 40px;
            width: 100%;
            max-width: 650px;
            box-shadow: var(--shadow);
            border-radius: 8px; /* Slight rounding contrasts the harsh borders */
        }
        h2 {
            margin-top: 0;
            font-size: 32px;
            font-weight: 900;
            text-transform: uppercase;
            background-color: var(--accent-purple);
            display: inline-block;
            padding: 8px 16px;
            border: 3px solid var(--border-color);
            box-shadow: 4px 4px 0px var(--border-color);
            transform: rotate(-2deg);
            letter-spacing: -1px;
        }
        p {
            font-family: system-ui, -apple-system, sans-serif;
            font-weight: 700;
            font-size: 16px;
            margin-bottom: 25px;
            margin-top: 20px;
        }
        textarea {
            width: 100%;
            height: 180px;
            background-color: #f8fafc;
            border: 3px solid var(--border-color);
            padding: 16px;
            font-family: system-ui, -apple-system, sans-serif;
            font-size: 16px;
            font-weight: 500;
            resize: vertical;
            box-sizing: border-box;
            margin-bottom: 20px;
            box-shadow: 4px 4px 0px var(--border-color);
            outline: none;
            transition: all 0.15s ease;
            line-height: 1.5;
        }
        textarea:focus {
            transform: translate(2px, 2px);
            box-shadow: var(--shadow-pressed);
            background-color: #ffffff;
        }
        button {
            background-color: var(--accent-green);
            color: #000;
            border: 3px solid var(--border-color);
            padding: 16px 24px;
            font-size: 18px;
            font-weight: 900;
            text-transform: uppercase;
            cursor: pointer;
            width: 100%;
            box-shadow: var(--shadow);
            transition: all 0.1s ease-out;
            letter-spacing: 1px;
        }
        button:hover {
            background-color: #22c55e;
            transform: translate(-2px, -2px);
            box-shadow: 8px 8px 0px var(--border-color);
        }
        button:active {
            transform: translate(4px, 4px);
            box-shadow: var(--shadow-pressed);
        }
        button:disabled {
            background-color: #cbd5e1;
            cursor: not-allowed;
            transform: translate(4px, 4px);
            box-shadow: var(--shadow-pressed);
        }
        #output {
            margin-top: 30px;
            padding: 20px;
            background-color: var(--accent-orange);
            border: 3px solid var(--border-color);
            box-shadow: 4px 4px 0px var(--border-color);
            min-height: 80px;
            white-space: pre-wrap;
            font-family: system-ui, -apple-system, sans-serif;
            font-size: 16px;
            font-weight: 600;
            display: none; 
            line-height: 1.6;
        }
        .thinking {
            display: inline-block;
            font-family: 'Courier New', Courier, monospace;
            font-weight: 900;
            animation: bounce 0.8s infinite;
        }
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-4px); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>AI Humanizer</h2>
        <p>DROP YOUR ROBOTIC TEXT BELOW.</p>
        
        <textarea id="inputText" placeholder="Paste text here..."></textarea>
        <button id="actionBtn" onclick="humanize()">HUMANIZE TEXT</button>

        <div id="output"></div>
    </div>

    <script>
        async function humanize() {
            const text = document.getElementById('inputText').value;
            if (!text.trim()) return;

            const outputDiv = document.getElementById('output');
            const btn = document.getElementById('actionBtn');
            
            outputDiv.style.display = 'block';
            outputDiv.innerHTML = '<span class="thinking">PROCESSING...</span>';
            btn.disabled = true;
            btn.innerText = "WORKING...";

            try {
                const response = await fetch('/humanize', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });

                const data = await response.json();
                outputDiv.innerText = data.humanized_text || "An error occurred.";
            } catch (err) {
                outputDiv.innerText = "ERROR: CONNECTION FAILED.";
            } finally {
                btn.disabled = false;
                btn.innerText = "HUMANIZE TEXT";
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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    } 
    system_prompt = """You are a highly creative, slightly erratic human writer. Your only goal is to bypass AI detection algorithms (like ZeroGPT).
    Rules to break the mathematical signature of AI:
    1. Subjective Framing: Use phrases like "Honestly," "I think," "To be fair," or "Look." AI rarely does this naturally.
    2. Imperfect Flow: Start sentences with conjunctions (And, But, Or, Because). Use run-on sentences occasionally. 
    3. Idiomatic Language: Use common human idioms and figures of speech.
    4. Banned Vocabulary: NO words like delve, testament, tapestry, realm, moreover, intricate, crucial, or multifaceted.
    5. Structural Chaos: Drastically mix 2-word sentences with 40-word wandering sentences. 
    Output ONLY the rewritten text. No intros, no quotes around the output.
    6. Punctuation Ban: DO NOT use hyphens (-), em-dashes (—), colons (:), semicolons (;), or asterisks (*). Stick strictly to commas, periods, and question marks.
    7. Extreme Burstiness: Vary sentence length drastically. Mix 3-word fragments with long, flowing sentences.
    8. Unpredictable Punctuation: Use punctuation in unconventional ways, like multiple question marks??? or ellipses... but only if it feels natural.
    9. Strict Typographic Spacing: Ensure flawless spacing. Absolutely NO double spaces. Punctuation marks MUST be immediately followed by a single space, with no space before them.
    """
    payload = {
        "model":"llama-3.3-70b-versatile",
        "temperature": 0.8, 
        "messages": [
            {
                "role": "system",
                "content": "Rewrite this text to sound like a real human wrote it on a blog. Use casual, everyday language. Change the vocabulary entirely. Keep it punchy."
            },
            {
                "role": "user",
                "content": data.text
            }
        ]
    }
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
            return {"humanized_text": result["choices"][0]["message"]["content"]}           
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return {"humanized_text": f"HTTP Error {e.code}: {error_body}"}
    except Exception as e:
        return {"humanized_text": f"Raw Network Error: {repr(e)}"}