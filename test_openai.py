import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read the API key
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("OpenAI API key loaded successfully!")
else:
    print("API key not found. Check your .env file.")