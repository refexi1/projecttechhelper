import gradio as gr
from ai_service import MODEL_ID, ai_service


def chat_reply(message: str, history) -> str:
    return ai_service(message)


demo = gr.ChatInterface(
    fn=chat_reply,
    title="Expert IT support assistant",
    description=(
        f"Running with local model: {MODEL_ID}. "
        "Answers may be incorrect; check official university information."
    ),
    examples=[
        "My Application won't start. What should I do?",
        "My laptop won't turn on. What should I do?",
    ],
)

if __name__ == "__main__":
    demo.launch(share=False)