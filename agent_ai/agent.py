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
async def explain_agent(instruction: str) -> str:
    agent = Agent(
        name = "Assistant",
        instructions = "You are a helpful Assistant that Explains the todo from the list.",
        tools = [],
        model=OpenAIChatCompletionsModel(
            openai_client=client,
            model="gemini-2.0-flash",
        ),
    )
    result = await Runner.explain(agent, instruction.join(" ", "Explain in detail Answer."))
    return result
async def run_agent(instruction: str) -> str:
    agent = Agent(
        name = "Assistant",
        instructions = "You are a helpful Assistant that manages Todos list.",
        tools = [get_todos,get_todo_by_id],
        # handoffs=[explain_agent],
        model=OpenAIChatCompletionsModel(
            openai_client=client,
            model="gemini-2.0-flash",
        ),
    )
    result = await Runner.run(
        agent,
        instruction,
    )
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
@function_tool
def get_todo_by_id(todo_id: int):
    """
    Retrieves a Todo item by its ID.

    Args:
        todo_id (int): The ID of the Todo item.

    Returns:
        Dict: The Todo item details.
    """
    result = requests.get(f"http://127.0.0.1:8000/todos/{todo_id}")
    if result.status_code == 200:
        return result.json()
    else:
        raise Exception(f"Failed to retrieve todo: {result.status_code}")

# @function_tool
# def delete_todo(todo_id: int):
#     """
#     Deletes a Todo item by its ID.

#     Args:
#         todo_id (int): The ID of the Todo item to delete.

#     Returns:
#         bool: True if the deletion was successful, False otherwise.
#     """
#     result = requests.delete(f"http://127.0.0.1:8000/todos/{todo_id}")
#     return result.status_code == 204

if __name__ == "__main__":
    # print(get_todos())
    while True:
        instruction = input("You:-> ")
        if instruction.lower() == "exit":
            break
        result = asyncio.run(run_agent(instruction))
        print("Assistant:->", result)