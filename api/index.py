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

# Neo-Brutalist UI with Floating Side Elements & Fluid Typing
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Humanizer | Neo-Brutalist</title>
    <style>
        :root {
            --bg-color: #f7f3e9; 
            --app-bg: #ffffff;
            --border-color: #000000;
            --accent-purple: #bb86fc;
            --accent-green: #03dac6;
            --accent-orange: #ffab91;
            --text-main: #1a1a1a;
            --shadow: 10px 10px 0px var(--border-color);
            --shadow-pressed: 4px 4px 0px var(--border-color);
        }
        body {
            font-family: 'Courier New', Courier, monospace;
            background-color: var(--bg-color);
            background-image: radial-gradient(#aaa 1px, transparent 1px);
            background-size: 25px 25px;
            color: var(--text-main);
            min-height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 40px;
            position: relative;
            overflow-x: hidden;
        }
        
        /* Floating Side Elements */
        .deco {
            position: fixed;
            border: 4px solid var(--border-color);
            box-shadow: 6px 6px 0px var(--border-color);
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: 900;
            z-index: -1;
        }
        .deco-1 { top: 15%; left: 8%; width: 100px; height: 100px; background-color: var(--accent-orange); transform: rotate(-10deg); font-size: 28px; }
        .deco-2 { bottom: 20%; right: 8%; width: 120px; height: 60px; background-color: var(--accent-purple); transform: rotate(5deg); font-size: 22px; }
        .deco-3 { top: 20%; right: 12%; width: 80px; height: 80px; background-color: var(--accent-green); border-radius: 50%; transform: rotate(15deg); font-size: 40px; }
        .deco-4 { bottom: 15%; left: 12%; width: 80px; height: 80px; background-color: #fff; transform: rotate(-5deg); font-size: 50px; }
        
        /* Hide decorations on smaller screens to keep it clean */
        @media (max-width: 1000px) {
            .deco { display: none; }
        }

        .container {
            background-color: var(--app-bg);
            border: 6px solid var(--border-color);
            padding: 50px;
            width: 100%;
            max-width: 700px;
            box-shadow: var(--shadow);
            border-radius: 4px;
            position: relative;
            z-index: 10;
        }
        .container::before { 
            content: '';
            position: absolute;
            top: -12px;
            left: -12px;
            width: 30px;
            height: 30px;
            background-color: var(--border-color);
        }
        h2 {
            margin-top: 0;
            font-size: 36px;
            font-weight: 900;
            text-transform: uppercase;
            background-color: var(--accent-purple);
            display: inline-block;
            padding: 10px 20px;
            border: 4px solid var(--border-color);
            box-shadow: 6px 6px 0px var(--border-color);
            transform: rotate(-3deg);
            letter-spacing: -1.5px;
        }
        p {
            font-family: system-ui, -apple-system, sans-serif;
            font-weight: 800;
            font-size: 18px;
            margin-bottom: 30px;
            margin-top: 25px;
        }
        textarea {
            width: 100%;
            height: 200px;
            background-color: #fafafa;
            border: 4px solid var(--border-color);
            padding: 20px;
            font-family: system-ui, -apple-system, sans-serif;
            font-size: 17px;
            font-weight: 500;
            resize: vertical;
            box-sizing: border-box;
            margin-bottom: 25px;
            box-shadow: 6px 6px 0px var(--border-color);
            outline: none;
            transition: all 0.2s ease;
            line-height: 1.6;
        }
        textarea:focus {
            transform: translate(3px, 3px);
            box-shadow: var(--shadow-pressed);
            background-color: #ffffff;
        }
        button {
            background-color: var(--accent-green);
            color: #000;
            border: 4px solid var(--border-color);
            padding: 18px 30px;
            font-size: 20px;
            font-weight: 900;
            text-transform: uppercase;
            cursor: pointer;
            width: 100%;
            box-shadow: var(--shadow);
            transition: all 0.15s ease-out;
            letter-spacing: 1.5px;
        }
        button:hover {
            background-color: #01b4a1;
            transform: translate(-3px, -3px);
            box-shadow: 13px 13px 0px var(--border-color);
        }
        button:active {
            transform: translate(7px, 7px);
            box-shadow: var(--shadow-pressed);
        }
        button:disabled {
            background-color: #b0bec5;
            cursor: not-allowed;
            transform: translate(7px, 7px);
            box-shadow: var(--shadow-pressed);
        }
        #output {
            margin-top: 40px;
            padding: 25px;
            background-color: var(--accent-orange);
            border: 4px solid var(--border-color);
            box-shadow: 6px 6px 0px var(--border-color);
            min-height: 100px;
            white-space: pre-wrap;
            font-family: system-ui, -apple-system, sans-serif;
            font-size: 17px;
            font-weight: 700;
            display: none; 
            line-height: 1.7;
        }
        .thinking {
            display: inline-block;
            font-family: 'Courier New', Courier, monospace;
            font-weight: 900;
            animation: bounce 0.9s infinite;
        }
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }
    </style>
</head>
<body>

    <div class="deco deco-1">TXT</div>
    <div class="deco deco-2">SYS_</div>
    <div class="deco deco-3">★</div>
    <div class="deco deco-4">" "</div>

    <div class="container">
        <h2>AI Humanizer</h2>
        <p>DROP YOUR ROBOTIC TEXT BELOW.</p>
        
        <textarea id="inputText" placeholder="Paste text here..."></textarea>
        <button id="actionBtn" onclick="humanize()">HUMANIZE TEXT</button>

        <div id="output"></div>
    </div>

    <script>
        // Fluid Typewriter Function
        async function typeWriter(text, element, speed = 15) {
            element.innerHTML = '';
            for (let i = 0; i < text.length; i++) {
                element.innerHTML += text.charAt(i);
                // Wait for 'speed' milliseconds before typing the next character
                await new Promise(resolve => setTimeout(resolve, speed));
            }
        }

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
                
                if (data.humanized_text && !data.humanized_text.startsWith("Error")) {
                    // Call the fluid typing effect
                    await typeWriter(data.humanized_text, outputDiv, 15);
                } else {
                    outputDiv.innerText = data.humanized_text || "An error occurred.";
                }
                
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
    Output ONLY the rewritten text. No intros, no quotes around the output."""

    payload = {
        "model": "llama-3.3-70b-versatile", 
        "messages": [
            {
                "role": "system",
                "content": system_prompt
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