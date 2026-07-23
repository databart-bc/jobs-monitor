import os

from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("JOOBLE_API_KEY")
base_url = os.getenv("JOOBLE_BASE_URL")

print(f"JOOBLE_API_KEY ustawiony: {bool(api_key)}")
print(f"JOOBLE_BASE_URL: {base_url}")