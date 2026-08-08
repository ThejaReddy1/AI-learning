# 45-Day AI Challenge

This repository contains Python experiments for learning prompt engineering, structured prompting, tool calling, and Google ADK agent workflows. It was created as part of a hands-on 45-day AI learning challenge.

## Project Overview

The project includes example scripts that demonstrate:

- Calling Gemini/GenAI models with the Google GenAI SDK
- Prompt engineering patterns such as zero-shot, few-shot, and system instructions
- Function/tool calling and JSON-constrained model responses
- Experimenting with temperature to compare deterministic and creative outputs
- Google ADK agent orchestration with `Agent`, `Runner`, and session state

## Repository Structure

- [main.py](main.py) — compares output for the same prompt at different temperatures
- [day_2_prompt_patterns.py](day_2_prompt_patterns.py) — demonstrates zero-shot, few-shot, and system prompt strategies
- [day_3_tool_calling.py](day_3_tool_calling.py) — shows how to define a tool function and let the model invoke it via function declaration
- [day4_agent_loop.py](day4_agent_loop.py) — explains how the agent loop works under the hood using raw Python and model API calls
- [day5_adk.py](day5_adk.py) — builds the `Agent`, `Runner`, and `InMemorySessionService` workflow for ADK agent execution
- [day_6_RAG_fundamentales.py](day_6_RAG_fundamentales.py) — demonstrates retrieval-augmented generation (RAG) with embeddings, similarity search, and context-augmented prompting
- [requirements.txt](requirements.txt) — Python dependency pins for the project
- [pyproject.toml](pyproject.toml) — project metadata and dependency configuration

## Requirements

- Python 3.14+
- A valid Google Gemini / Google GenAI API key

## Setup

1. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root and add your API key:

   ```env
   API_KEY=your_google_gemini_api_key_here
   ```

3. Activate your Python environment if using a virtual environment:

   ```bash
   .venv\Scripts\activate
   ```

## Usage

Run the example scripts directly with Python:

```bash
python main.py
python day_2_prompt_patterns.py
python day_3_tool_calling.py
python day4_agent_loop.py
python day5_adk.py
python day_6_RAG_fundamentales.py
```

If you are using `uv`, these commands also work with:

```bash
uv run python main.py
uv run python day_2_prompt_patterns.py
uv run python day_3_tool_calling.py
uv run python day4_agent_loop.py
uv run python day5_adk.py
uv run python day_6_RAG_fundamentales.py
```

## Notes

- The project uses `google-adk`, `adk`, and `dotenv` for Google ADK/GenAI integration and environment loading.
- The scripts are learning examples and not intended for production deployment.
- Model output can vary with prompt design, temperature, and model selection.
- Keep your API key secret and do not commit `.env` to version control.
