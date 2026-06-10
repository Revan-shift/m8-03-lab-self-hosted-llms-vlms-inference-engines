"""
local_client.py — Calls a locally-running Ollama model via its OpenAI-compatible endpoint.

WHY THIS IS "THE SAME SHAPE" AS A HOSTED API CALL:
----------------------------------------------------
Yesterday we called Gemini (a hosted API) by sending an HTTP POST request to
Google's servers with a JSON body containing a model name, a prompt, and some
parameters — and got a JSON response back with the generated text.

Today we're doing *exactly the same thing*, but the HTTP request goes to
http://localhost:11434 instead of a remote server. Ollama exposes an
OpenAI-compatible `/v1/chat/completions` endpoint, so the request shape
(headers, body, response format) is identical. The Python `openai` SDK doesn't
know or care whether the server is on Google's infrastructure or on your laptop
— it's just an HTTP client. The *inference server* changed; the *protocol* did
not. This is why "calling an LLM" is really just sending a JSON request to an
inference server, wherever that server happens to run.
"""

from openai import OpenAI

# Point the OpenAI client at our LOCAL Ollama server instead of api.openai.com
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama doesn't require a real key; any non-empty string works
)

MODEL = "llama3.2:3b"  # Change to "qwen2.5:0.5b" if resources are tight
PROMPT = "Explain what a large language model is in 3 sentences."

def main():
    print(f"Sending prompt to local model: {MODEL}")
    print(f"Prompt: {PROMPT}\n")
    print("-" * 50)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": PROMPT}
        ],
        temperature=0.7,
    )

    answer = response.choices[0].message.content
    print("Model response:")
    print(answer)
    print("-" * 50)

    # Print token usage if available
    if response.usage:
        print(f"\nTokens used — Prompt: {response.usage.prompt_tokens}, "
              f"Completion: {response.usage.completion_tokens}, "
              f"Total: {response.usage.total_tokens}")

if __name__ == "__main__":
    main()
