import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("JOOBLE_API_KEY")
base_url = os.getenv("JOOBLE_BASE_URL")

if not api_key:
    raise RuntimeError("Brak JOOBLE_API_KEY w pliku .env")

payload = {
    "keywords": "Data Engineer",
    "location": "Poland",
    "page": 1,
    "ResultOnPage": 10,
}

response = requests.post(
    url=f"{base_url}/{api_key}",
    json=payload,
    timeout=30,
)

response.raise_for_status()
data = response.json()

output_directory = Path("data/bronze/jooble")
output_directory.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
output_path = output_directory / f"jooble_{timestamp}.json"

with output_path.open("w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print(f"Pobrano ofert: {len(data.get('jobs', []))}")
print(f"Zapisano plik: {output_path.resolve()}")