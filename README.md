# Project TechHelper

All data about our project.

## Team members

- YASER AL-DALAWI (yaser.al-dalawi@student.hamk.fi).yasserdalawi401@gmail.com
- Vesa Wahlström (vesa.wahlstrom@student.hamk.fi)
- Nuutti Tikka (nuutti.tikka@student.hamk.fi)
- Sanna Poikonen (sanna.poikonen@student.hamk.fi)

## Team Responsibilities

### Yaser Al-Dalawi – Testing and Evaluation
- Develops and maintains tests for the application.
- Evaluates the quality and usefulness of AI-generated troubleshooting responses.
- Helps document testing procedures and evaluation results.

### Vesa Wahlström – User Interface
- Develops the user interface for the application.
- Works on making the chat interface clear and easy to use.
- Integrates the interface with the AI service.

### Nuutti Tikka – AI Service and Language Model Integration
- Integrates the locally running Llama 3.2 language model using Ollama.
- Develops the system prompt to guide the AI's troubleshooting responses.
- Implements JSON response handling and connects the AI service to the response validation system.
- Adds retry logic and error handling for invalid AI responses.
- Tests the AI service and its integration with the application.

### Sanna Poikonen – Data Schemas and Response Validation
- Defines the structure of AI responses using Pydantic.
- Implements validation for the required response fields: `problem`, `os_type`, and `steps`.
- Develops tests to verify that valid responses are accepted and invalid responses are rejected.
- Helps ensure that AI responses follow the expected data structure.


### Application

Creating an application for users who need help with technical difficulties through an easy-to-use interface. Our app focuses on popular operating systems such as Windows 11, macOS, Linux distributions, and Android/iOS devices.

### Why this application is needed

Many users encounter various issues with computers, laptops, mobile devices, and software applications. An AI assistant dedicated to troubleshooting these issues, from "PC won't turn on" to "This software is not functioning correctly," could help users find possible solutions. The application presents responses in a structured JSON format through a readable user interface, making the troubleshooting process easier to follow.

### Why use AI in this application

AI is useful because the application needs to support different operating systems, devices, and software problems. A language model can interpret users' descriptions of their problems and generate relevant troubleshooting instructions. This provides flexibility when responding to different situations. The responses are structured and validated to improve consistency, although the suggested solutions may not always be correct.

## Main user workflow

1. **Describe the problem:** The user enters a technical problem into the application's chat interface.
2. **Analyze the request:** The AI service processes the user's description using a locally running language model.
3. **Generate a solution:** The model generates a structured response containing the problem description, operating system, and troubleshooting steps.
4. **Validate the response:** The application validates the response structure and required fields using Pydantic. If the response is invalid, the AI service attempts to generate a valid response again.
5. **Display the result:** The application displays the troubleshooting response in the user interface.
6. **Follow the instructions:** The user reviews the suggested steps and tries the relevant solutions.

## Main features

- User-friendly chat interface for describing technical problems.
- AI-generated troubleshooting instructions.
- Support for common computer, operating system, and software problems.
- Structured JSON responses with three fields: `problem`, `os_type`, and `steps`.
- Response validation using Pydantic.
- Retry logic for invalid AI responses.
- Basic error handling when a valid response cannot be generated.
- Local language model execution using Ollama and Llama 3.2.

## Technology stack

- **Programming language:** Python
- **Language model:** Llama 3.2
- **Local model runtime:** Ollama
- **User interface:** Gradio
- **Data validation:** Pydantic
- **Testing:** Pytest
- **Version control and collaboration:** Git and GitHub

## AI service and response format

The AI service receives a user's question and sends it to the language model together with a system prompt. The prompt instructs the model to provide safe, practical, and ordered troubleshooting steps in a specific JSON format.

The response must contain the following fields:

- `problem`: A short description of the technical problem.
- `os_type`: The operating system involved, or `Unknown` if it has not been specified.
- `steps`: A list of practical troubleshooting instructions.

Pydantic validates the response to ensure that the required fields contain appropriate non-empty values. If validation fails, the service retries the request once before returning an error message.

## Testing and evaluation

The application is tested to verify that its response validation works correctly. Pytest tests cover both valid and invalid AI responses.

The testing process checks that:
- Valid JSON responses are accepted.
- Invalid responses are rejected.
- Required fields and troubleshooting steps meet the validation rules.
- The application can be started and tested locally.

The current validation tests have passed. Further testing is needed to evaluate the accuracy, usefulness, and safety of the AI-generated troubleshooting advice across different technical problems and operating systems.

## Limitations and safety

The application provides AI-generated suggestions, not guaranteed solutions. The model may misunderstand a problem or provide incorrect instructions. Response validation checks the structure and required fields, but it does not guarantee that the technical advice is factually correct.

Users should review the instructions carefully and consult official documentation or technical support when necessary. Potentially destructive actions should not be recommended as initial troubleshooting steps.

## Project goal

The goal of Project TechHelper is to develop an accessible AI-powered technical support application that helps users understand common technical problems and find practical troubleshooting steps through a simple chat interface.

The project also demonstrates how a locally running language model can be integrated into a Python application with structured responses, data validation, error handling, and automated tests.


