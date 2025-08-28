import requests
import json
import os

MODEL = "gpt-oss:20b"
API_URL = "http://localhost:11434/api/generate"
SAVE_FILE = "findings.json"

# Load previous history if file exists
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        conversation = json.load(f)
else:
    conversation = []

print(f"💬 Interactive chat with {MODEL}")
print("Type /exit to quit\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["/exit", "exit", "quit", "/quit"]:
        print("👋 Goodbye!")
        break

    payload = {
    "model": MODEL,
    "prompt": f"Answer in under 2000 words:\n{user_input}",
    "num_predict": 2600, 
    "stream": True
    }

    try:
        response_text = ""
        response = requests.post(API_URL, json=payload, stream=True)
        print("AI: ", end="", flush=True)
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    chunk = data["response"]
                    response_text += chunk
                    print(chunk, end="", flush=True)
        print("\n")

        conversation.append({"question": user_input, "answer": response_text})

        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(conversation, f, ensure_ascii=False, indent=2)

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
