

from services.groq_client import call_groq

def test_basic_call():
    messages = [
        {"role": "user", "content": "Say hello in one sentence"}
    ]
    result = call_groq(messages)
    print("Result:", result)

    if result["is_fallback"]:
        print("Fallback returned — check your API key")
    else:
        print("GroqClient working!")
        print("Response:", result["content"])

if __name__ == "__main__":
    test_basic_call()
