import requests
def fetch_jooble_jobs(
    api_key: str,
    base_url: str,
    payload: dict,
) -> tuple[dict, int]:
    response = requests.post(
        url=f"{base_url}/{api_key}",
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    return response.json(), response.status_code