import json
import sys
import urllib.request
import urllib.error

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:latest"


def generate_response(prompt: str, model: str = MODEL_NAME) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=600) as response:
            result = json.load(response)
            return result.get("response", "")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed to connect to Ollama at {OLLAMA_URL}: {exc}") from exc


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Write a short greeting in one sentence."
    response = generate_response(prompt)
    print(response)
