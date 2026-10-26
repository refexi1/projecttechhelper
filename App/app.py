import json
import gradio as gr
from ai_service import MODEL_ID, ai_service

def chat_reply(message: str, history, os_choice: str) -> str:
    """
    Combines the OS selection with the user message, calls ai_service,
    and formats the resulting JSON nicely for the Gradio chat interface.
    """
    if not message.strip():
        return "Please enter a problem description."
    
    # Format the prompt with the user's OS choice so the AI receives it
    enhanced_message = (
        f"Operating System: {os_choice}\n"
        f"Problem: {message}"
    )
    
    # Call your friend's ai_service (which returns a JSON string)
    raw_response = ai_service(enhanced_message)
    
    try:
        # Parse the JSON returned by ai_service
        data = json.loads(raw_response)
        
        # Format the JSON nicely into human-readable text for the UI chat box
        problem = data.get("problem", "N/A")
        os_type = data.get("os_type", "N/A")
        steps = data.get("steps", [])
        
        # Build a neat markdown response
        formatted_reply = f"###  Problem Summary\n{problem}\n\n"
        formatted_reply += f" **OS Detected:** {os_type}\n\n"
        formatted_reply += "###  Troubleshooting Steps:\n"
        for i, step in enumerate(steps, 1):
            formatted_reply += f"{i}. {step}\n"
            
        return formatted_reply

    except json.JSONDecodeError:
        # Fallback if the response wasn't valid JSON (e.g., error message)
        return raw_response


with gr.Blocks() as demo:
    gr.Markdown("# TechHelper - IT Support Assistant")
    gr.Markdown(f"Model: `{MODEL_ID}` | Select your OS and describe your technical issue.")
    
    with gr.Row():
        os_dropdown = gr.Dropdown(
            choices=[
                "Windows 11", 
                "Windows 10", 
                "macOS", 
                "Linux (Ubuntu/Debian)", 
                "Linux (Fedora/Arch)", 
                "Android", 
                "iOS", 
                "Unknown"
            ],
            value="Windows 11",
            label="Operating System",
            interactive=True
        )

    chat_ui = gr.ChatInterface(
        fn=chat_reply,
        additional_inputs=[os_dropdown],
        additional_inputs_accordion=gr.Accordion(" Settings", open=True),
        examples=[
            ["My application crashes on startup. What should I do?", "Windows 11"],
            ["How do I connect to an external display?", "macOS"],
            ["My Wi-Fi connection keeps dropping.", "Linux (Ubuntu/Debian)"],
        ],
        title=None,
        description=None
    )

if __name__ == "__main__":
    demo.launch(share=False, theme=gr.themes.Soft())
