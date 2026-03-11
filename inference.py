import anthropic
from config import Config

def create_client():
    return anthropic.Anthropic(api_key=Config.API_KEY)

def chat(client, messages):
    response = client.messages.create(
        model=Config.MODEL_NAME,
        max_tokens=Config.MAX_TOKENS,
        temperature=Config.TEMPERATURE,
        top_p=Config.TOP_P,
        system=Config.SYSTEM_PROMPT,
        messages=messages
    )
    return response.content[0].text

if __name__ == "__main__":
    client = create_client()
    messages = []
    
    print("LUMEN chat started. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        
        messages.append({"role": "user", "content": user_input})
        response = chat(client, messages)
        messages.append({"role": "assistant", "content": response})
        
        print(f"LUMEN: {response}\n")
