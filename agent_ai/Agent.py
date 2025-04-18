from dotenv import load_dotenv
import os
import requests
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner,set_tracing_disabled, function_tool

message: str = """
show - todo display all todos in a structured table format.\n
exit - exit the program.\n
"""

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
            model="gemini-1.5-flash",
        ),
    )
    result = await Runner.explain(agent, instruction.join(" ", "Explain in detail Answer."))
    return result
async def run_agent(instruction: str) -> str:
    agent = Agent(
        name = "Assistant",
        instructions = "You are a helpful Assistant that manages Todos list.",
        tools = [get_todos,get_todo_by_id,delete_todo_by_id,add_new_todo,update_a_todo_by_id],
        # handoffs=[explain_agent],
        model=OpenAIChatCompletionsModel(
            openai_client=client,
            model="gemini-1.5-flash",
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

@function_tool
def delete_todo_by_id(todo_id: int):
    """
    Deletes a Todo item by its ID.

    Args:
        todo_id (int): The ID of the Todo item to delete.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    result = requests.delete(f"http://127.0.0.1:8000/todos/{todo_id}")
    if result.status_code == 200:
        return "Todo deleted successfully"
    elif result.status_code == 404:
        return "Todo not found"
    else:
        raise Exception(f"Failed to delete todo: {result.status_code}")

@function_tool
def add_new_todo(title: str, description: str):
    """
    Adds a new Todo item.

    Args:
        title (str): The title of the Todo item to add.
        description (str): The description of the Todo item to add.

    Returns:
        str: A message indicating the result of the addition.
    """
    result = requests.post("http://127.0.0.1:8000/todos/", json={"title": title, "description": description})
    if result.status_code == 200:
        return "Todo added successfully"
    else:
        raise Exception(f"Failed to add todo: {result.status_code}")

@function_tool
def update_a_todo_by_id(todo_id: int, title: str, description: str):
    """
    Updates a Todo item by its ID.

    Args:
        todo_id (int): The ID of the Todo item to update.
        title (str): The new title for the Todo item.
        description (str): The new description for the Todo item.

    Returns:
        str: A message indicating the result of the update.
    """
    result = requests.put(f"http://127.0.0.1:8000/todos/{todo_id}/", json={"title": title, "description": description})
    if result.status_code == 200:
        return "Todo updated successfully"
    else:
        raise Exception(f"Failed to update todo: {result.status_code}")
                          

def chat(instruction: str) -> str:
    """
    Chat with the Assistant.

    Args:
        instruction (str): The instruction to send to the Assistant.

    Returns:
        str: The Assistant's response.
    """
    while True:
        if instruction.lower() == "exit":
            break
        if instruction.lower() == "show":
            instruction = "show - todo display all todos in a structured table format"
        result = asyncio.run(run_agent(instruction))
    return result
