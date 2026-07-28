# 45-Day AI Challenge

This repository contains a small set of Python experiments for learning prompt engineering, structured prompting, and tool calling with Google Gemini models. It was created as part of a hands-on 45-day AI challenge.

## Project Overview

The project includes simple example scripts that demonstrate:

- basic Gemini API usage
- prompt pattern techniques such as zero-shot, few-shot, and system instructions
- tool/function calling with a minimal calculator example
- temperature-based response behavior

## Repository Structure

- [main.py](main.py) — compares model responses at different temperatures for the same prompt
- [day_2_prompt_patterns.py](day_2_prompt_patterns.py) — demonstrates zero-shot, few-shot, and system prompt strategies
- [day_3_tool_calling.py](day_3_tool_calling.py) — shows how to define a tool and let the model call it
- [requirements.txt](requirements.txt) — Python dependencies for the project
- [pyproject.toml](pyproject.toml) — project metadata and dependency configuration

## Requirements

- Python 3.14+
- A valid Google Gemini API key

## Setup

1. Install uv if you do not already have it:

   ```bash
   pip install uv
   ```

2. Create and sync the environment with uv:

   ```bash
   uv venv
   uv sync
   ```

3. Activate the virtual environment:

   ```bash
   .venv\Scripts\activate
   ```

4. Create a `.env` file in the project root and add your API key:

   ```env
   API_KEY=your_google_gemini_api_key_here
   ```

## Usage

Run each example script individually with uv:

```bash
uv run python main.py
uv run python day_2_prompt_patterns.py
uv run python day_3_tool_calling.py
```

## Notes

- These scripts rely on the Google GenAI SDK and require network access to call the Gemini API.
- The examples are intentionally simple and meant for learning rather than production use.
- Model behavior may vary depending on the selected model and temperature settings.
