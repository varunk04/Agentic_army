import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_token = os.getenv("OPENROUTER_API_KEY")

response = requests.get(
  url="https://openrouter.ai/api/v1/auth/key",
  headers={
    "Authorization": f"Bearer {api_token}"
  }
)

print(json.dumps(response.json(), indent=2))
