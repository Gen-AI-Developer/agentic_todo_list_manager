
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()
# Set up the API key and endpoint
api_key = os.getenv("GEMINI_API_KEY")
