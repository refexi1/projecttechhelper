
import json
import re

from ollama import Client

MODEL_ID = "llama3.2:latest"
OLLAMA_HOST = "http://localhost:11434"

SYSTEM_MESSAGE = """
You are an expert IT support assistant.

Help users troubleshoot IT and software problems safely.
Return ONLY one valid JSON object. Do not include Markdown fences,
introductions, or text outside the JSON.

The JSON must have exactly these fields:
{
  "problem": "Short description of the user's problem",
  "os_type": "Operating system, or 'Unknown' if not specified",
  "steps": [
    "A clear, practical troubleshooting step"
  ]
}

Requirements:
- All three fields are required.
- problem and os_type must be non-empty strings.
- steps must be a non-empty list of non-empty strings.
- Give safe, ordered, actionable troubleshooting steps.
- Do not recommend destructive actions such as reinstalling the
  operating system as an initial step.
- If the operating system is not stated, use "Unknown".
"""


def get_client() -> Client:
    """Create an Ollama client and check that the model is installed."""
    client = Client(host=OLLAMA_HOST, timeout=60.0)

    installed_models = {item.model for item in client.list().models}
    if MODEL_ID not in installed_models:
        raise RuntimeError(
            f"{MODEL_ID!r} is not installed. "
            "Check the output of `ollama list`."
        )

    return client


model_client = get_client()


def _extract_json(response_text: str) -> str:
    """Extract JSON from a model response, including optional code fences."""
    text = response_text.strip()

    # Remove a surrounding Markdown code fence, if present.
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)

    # Keep the JSON object if the model added text around it.
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("The model did not return a JSON object.")

    return text[start:end + 1]


def ai_service(question: str) -> str:
    """Return a JSON troubleshooting response validated by the project schema."""
    cleaned_question = (question or "").strip()

    if not cleaned_question:
        return "Please enter a question."

    try:
        # Import here so the module can still be imported before schemas.py
        # is available in the current project branch.
        from schemas import validate_ai_response
    except ImportError:
        return (
            "Configuration error: schemas.py is not available. "
            "Please check the project structure."
        )

    last_error = None

    for attempt in range(2):
        messages = [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": cleaned_question},
        ]

        if attempt == 1:
            messages.append({
                "role": "user",
                "content": (
                    "Your previous response was invalid. "
                    "Return only valid JSON with exactly the fields "
                    "problem, os_type, and steps. "
                    f"Validation error: {last_error}"
                ),
            })

        try:
            response = model_client.chat(
                model=MODEL_ID,
                messages=messages,
                stream=False,
                format="json",
            )

            json_text = _extract_json(response.message.content)
            validation = validate_ai_response(json_text)

            if validation["success"]:
                return json.dumps(
                    validation["data"],
                    ensure_ascii=False,
                    indent=2,
                )

            last_error = validation["error"]

        except Exception as error:
            last_error = str(error)

    return (
        "The AI service could not produce a valid troubleshooting response "
        "after two attempts. Please try again."
    )
