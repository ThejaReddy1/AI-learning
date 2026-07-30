from google.adk.agents.llm_agent import Agent
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

def add_two_numbers(a: int, b: int) -> int:
    """
    Adds two numbers together.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
    return a + b

def multipy_two_numbers(a: int, b: int) -> int:
    """
    Multiplies two numbers together.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The product of the two numbers.
    """
    return a * b

MathAgent = Agent(
    name="MathAgent",
    model="gemma-4-31b-it",
    description="A calculator that can add and multiply numbers",
    instruction="You are a calculator. Use the tools provided to compute answers. Never calculate manually.",
    tools=[add_two_numbers, multipy_two_numbers]
)

session_service = InMemorySessionService()

async def main():
    session = await session_service.create_session(app_name="calc_app", user_id="user1")
    runner = Runner(agent=MathAgent, app_name="calc_app", session_service=session_service)

    user_message = types.Content(role="user", parts=[types.Part(text="What is (12 + 8) multiplied by 3?")])

    async for event in runner.run_async(user_id="user1", session_id=session.id, new_message=user_message):
        print(event)

asyncio.run(main())



"""
The Runner, explained slowly

What problem it solves: you already built the six-step loop by hand in Day 5 — call model, check for function call, execute, feed result back, repeat. The Runner is ADK's implementation of exactly that loop. You don't call the model directly anymore; you hand your message to the Runner, and it drives the whole cycle for you, yielding you an event every time something happens along the way.

The three pieces you set up before running anything

1. InMemorySessionService — this holds the conversation history (your Day 5 history = [] list), but as a proper object instead of a plain list you manage yourself. "InMemory" means it lives only in RAM for this process run — nothing persisted to disk or a database. Fine for learning; in a real deployed agent you'd swap this for a persistent session service.

2. A session — one specific conversation thread, created via session_service.create_session(app_name=..., user_id=...). Think of app_name as "which agent app this is" and user_id as "whose conversation this is" — this is how ADK could support multiple users/conversations without you manually keeping separate history lists for each.

3. The Runner itself — takes your agent (the config: model + instructions + tools) and the session_service, and its job is: given a new message, drive the loop, updating the session's history as it goes.

What actually happens when you call runner.run_async(...)
python
async for event in runner.run_async(user_id=..., session_id=..., new_message=...):
    print(event)

This is an async generator — instead of returning one final answer, it yields you one event object every time something happens during the loop: a thought, a function call, a function response, or the final text. That's exactly what you saw printed — 4 separate events for your 2-tool-call question, corresponding one-to-one with your Day 5 loop's iterations.

Why async/await at all: network calls (to the Gemini API) take time, and async lets Python not sit frozen waiting — it's the standard pattern for any I/O-bound work like API calls. You don't need to master async deeply today, just recognize: async def main(), await before things that talk to the network, asyncio.run(main()) to kick it off — that's boilerplate you'll reuse constantly.

The one-sentence summary for your notes

Runner = your hand-built while True loop, running inside ADK, notifying you of every step via events instead of you printing your own debug lines.
"""
