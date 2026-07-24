import os
import json
import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("JOOBLE_API_KEY")
base_url = os.getenv("JOOBLE_BASE_URL")

if not api_key:
    raise RuntimeError("Missing JOOBLE_API_KEY in .env")

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

print(f"Total results: {data.get('totalCount')}")
print(f"Jobs retrieved: {len(jobs)}")

for job in jobs[:3]:
    print()
    print(f"Title: {job.get('title')}")
    print(f"Company: {job.get('company')}")
    print(f"Location: {job.get('location')}")
    print(f"Source: {job.get('source')}")

if jobs:
    print("\nFull first record:")
    print(json.dumps(jobs[0], ensure_ascii=False, indent=2))