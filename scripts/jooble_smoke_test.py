import os
import json
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
jobs = data.get("jobs", [])

print(f"Łączna liczba wyników: {data.get('totalCount')}")
print(f"Liczba pobranych ofert: {len(jobs)}")

for job in jobs[:3]:
    print()
    print(f"Stanowisko: {job.get('title')}")
    print(f"Firma: {job.get('company')}")
    print(f"Lokalizacja: {job.get('location')}")
    print(f"Źródło: {job.get('source')}")

if jobs:
    print("\nPełny pierwszy rekord:")
    print(json.dumps(jobs[0], ensure_ascii=False, indent=2))