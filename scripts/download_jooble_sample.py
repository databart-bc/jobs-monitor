import json
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from jobs_monitor.jooble import fetch_jooble_jobs

def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

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

data, http_status = fetch_jooble_jobs(
    api_key=api_key,
    base_url=base_url,
    payload=payload,
)

run_time = datetime.now(timezone.utc)

ingestion_date = run_time.strftime("%Y-%m-%d")
run_id = run_time.strftime("%Y%m%d_%H%M%S")

run_directory = (
    Path("data/bronze/jooble")
    / f"ingestion_date={ingestion_date}"
    / f"run_id={run_id}"
)

run_directory.mkdir(parents=True, exist_ok=True)

output_path = run_directory / "jobs.json"

save_json(output_path, data)

manifest = {
    "run_id": run_id,
    "source": "jooble",
    "ingestion_date": ingestion_date,
    "ingested_at_utc": run_time.isoformat(),
    "request": payload,
    "http_status": http_status,
    "total_count": data.get("totalCount"),
    "records_received": len(data.get("jobs", [])),
    "data_file": "jobs.json",
}

manifest_path = run_directory / "manifest.json"

save_json(manifest_path, manifest)

print(f"Jobs retrieved: {manifest['records_received']}")
print(f"Data saved to: {output_path.resolve()}")
print(f"Manifest saved to: {manifest_path.resolve()}")