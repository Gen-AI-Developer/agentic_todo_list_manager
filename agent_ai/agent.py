from dotenv import load_dotenv
import os
import requests
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner,set_tracing_disabled, function_tool
client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
set_tracing_disabled(True)

async def run_agent() -> str:
    agent = Agent(
        name = "Assistant",
        instructions = "You are a helpful Assistant that manages Todos list.",
        tools = [get_todos],
        model=OpenAIChatCompletionsModel(
            openai_client=client,
            model="gemini-2.0-flash",
        ),
    )
    result = await Runner.run(
        agent,
        "how Many todos are there in my list. can you list them out in a table? try to answer the 3rd todo?",)
    return result.final_output

@function_tool
def get_todos():
    """
    Retrieves a list of Todo items.

    Returns:
        List[Todo]: A list of Todo items.
    """
    result = requests.get("http://127.0.0.1:8000/todos/")
    if result.status_code == 200:
        return result.json()
    else:
        raise Exception(f"Failed to retrieve todos: {result.status_code}")

if __name__ == "__main__":
    # print(get_todos())
    print(asyncio.run(run_agent()))