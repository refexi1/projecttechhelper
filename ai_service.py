from ollama import Client

MODEL_ID = "qwen3:4b"  
OLLAMA_HOST = "http://localhost:11434"

SYSTEM_MESSAGE = (
    "You are an expert IT support assistant. "
    "Analyze the user's technical problem and operating system. "
    "Provide a structured troubleshooting guide in valid JSON format matching the required schema."
)


def get_client() -> Client:
    """Initializes and returns the Ollama client after running checks."""
    client = Client(host=OLLAMA_HOST, timeout=60.0)

    installed_models = {item.model for item in client.list().models}
    if MODEL_ID not in installed_models:
        raise RuntimeError(
            f"{MODEL_ID!r} is not installed. Run `ollama list`, "
            "choose an installed chat model, and update MODEL_ID."
        )

    capabilities = set(client.show(MODEL_ID).capabilities or [])
    if "completion" not in capabilities:
        raise RuntimeError(f"{MODEL_ID!r} does not support chat completion.")

    return client


# Global client instance initialized at startup
model_client = get_client()


def ai_service(question: str) -> str:
    """Processes the user question through the Ollama model."""
    cleaned_question = (question or "").strip()

    if not cleaned_question:
        return "Please enter a question."

    try:
        response = model_client.chat(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": cleaned_question},
            ],
            stream=False,
        )
        return response.message.content
    except Exception:
        return "The AI service could not complete the request. Please try again."