import requests

API_KEY = "YOUR_API_KEY"
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
MAX_HISTORY = 10  # Keep last 10 exchanges (user + AI)

def ask_ai(conversation_history):
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }

    # Prepare the conversation payload with roles
    contents = []
    for message in conversation_history:
        role = "user" if message["role"] == "user" else "assistant"
        contents.append({
            "parts": [{"text": message["text"]}],
            "role": role
        })

    data = {"contents": contents}

    response = requests.post(URL, json=data, headers=headers)
    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"

    try:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError):
        return "Unexpected response format"

if __name__ == "__main__":
    print("=== Gemini Chat ===")
    print("Type 'exit' to quit, 'reset' to clear conversation history.")

    conversation_history = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Ending conversation.")
            break
        if user_input.lower() == "reset":
            conversation_history = []
            print("Conversation history cleared.")
            continue

        # Append user message
        conversation_history.append({"role": "user", "text": user_input})

        # Trim history to last MAX_HISTORY exchanges
        if len(conversation_history) > MAX_HISTORY * 2:
            conversation_history = conversation_history[-MAX_HISTORY*2:]

        # Get AI response
        ai_response = ask_ai(conversation_history)
        print("AI:", ai_response)

        # Append AI response
        conversation_history.append({"role": "assistant", "text": ai_response})
      
