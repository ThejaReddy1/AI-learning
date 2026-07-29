# 45-Day AI Challenge

This repository contains Python experiments for learning prompt engineering, structured prompting, and tool calling with Google Gemini / Google GenAI models. It was created as part of a hands-on 45-day AI learning challenge.

## Project Overview

The project includes example scripts that demonstrate:

- Using the Google GenAI SDK to call Gemini-style models
- Prompt engineering patterns such as zero-shot, few-shot, and system instructions
- Function/tool calling with a calculator-style example
- Temperature-based response behavior and usage metadata
- An iterative agent loop with tool calls and response validation

## Repository Structure

- [main.py](main.py) — runs the same prompt at different temperatures to compare response variation
- [day_2_prompt_patterns.py](day_2_prompt_patterns.py) — demonstrates zero-shot, few-shot, and system prompt strategies
- [day_3_tool_calling.py](day_3_tool_calling.py) — shows how to define a tool and let the model call it through a function declaration
- [day4_agent_loop.py](day4_agent_loop.py) — extends tool calling into an agent loop with multiple tool functions and response history
- [requirements.txt](requirements.txt) — Python dependencies for the project
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
```

If you are using `uv`, the same commands work with:

```bash
uv run python main.py
uv run python day_2_prompt_patterns.py
uv run python day_3_tool_calling.py
uv run python day4_agent_loop.py
```

## Notes

- The project uses `google-adk` and `python-dotenv`.
- The scripts are learning examples and not intended for production deployment.
- Model output can vary with model choice, prompt structure, and temperature settings.
- Keep your API key secret and do not commit `.env` to version control.
