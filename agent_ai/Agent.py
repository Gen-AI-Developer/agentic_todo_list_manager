from dotenv import load_dotenv
import os
import requests
import asyncio
import time
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled, function_tool

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-exp:free"

# Initialize the OpenAI client with OpenRouter configuration
client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL,
    default_headers={
        "HTTP-Referer": "http://localhost:8000",  # Optional, for tracking
        "X-Title": "Todo List Manager",  # Optional, for tracking
    }
)
set_tracing_disabled(True)

# Rate limiting settings
REQUEST_LIMIT = 15  # requests per minute
request_times = []

async def wait_for_rate_limit():
    """
    Implements rate limiting to avoid hitting API limits.
    """
    current_time = time.time()
    # Remove requests older than 1 minute
    while request_times and current_time - request_times[0] >= 60:
        request_times.pop(0)
    
    if len(request_times) >= REQUEST_LIMIT:
        # Wait until we can make another request
        wait_time = 60 - (current_time - request_times[0])
        if wait_time > 0:
            await asyncio.sleep(wait_time)
        request_times.pop(0)
    
    request_times.append(current_time)

async def explain_agent(instruction: str) -> str:
    """
    Agent that explains todos in detail.

    Args:
        instruction (str): The instruction to explain.

    Returns:
        str: Detailed explanation of the todo.
    """
    await wait_for_rate_limit()
    
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful Assistant that Explains the todo from the list.",
        tools=[],
        model=OpenAIChatCompletionsModel(
            openai_client=client,
            model=MODEL,
        ),
    )
    # Fix the string concatenation
    result = await Runner.explain(agent, f"{instruction} Explain in detail Answer.")
    return result

async def run_agent(instruction: str) -> str:
    """
    Main agent that manages the todo list.

    Args:
        instruction (str): The instruction to process.

    Returns:
        str: The result of processing the instruction.
    """
    await wait_for_rate_limit()
    
    try:
        agent = Agent(
            name="Assistant",
            instructions="You are a helpful Assistant that manages Todos list.",
            tools=[get_todos, get_todo_by_id, delete_todo_by_id, add_new_todo, update_a_todo_by_id],
            model=OpenAIChatCompletionsModel(
                openai_client=client,
                model=MODEL,
            ),
        )
        result = await Runner.run(
            agent,
            instruction,
        )
        # Ensure we always return a string
        if result and hasattr(result, 'final_output'):
            return str(result.final_output) if result.final_output is not None else "Task completed but no output was returned"
        return "No response received from the agent"
    except Exception as e:
        print(f"Debug - Run agent error: {str(e)}")  # For debugging
        return f"Error processing request: {str(e)}"

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
    try:
        # Handle exit command
        if instruction.lower() == "exit":
            return "Goodbye! Thank you for using the Todo List Manager."
        
        # Handle show command
        if instruction.lower() == "show":
            instruction = "show - todo display all todos in a structured table format"
        
        # Run the agent and ensure we always return a string
        result = asyncio.run(run_agent(instruction))
        return result if result is not None else "No response from the agent"
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"Debug - Chat function error: {error_msg}")  # For debugging
        return error_msg
