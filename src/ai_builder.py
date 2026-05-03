import json
from datetime import datetime, UTC

from config.settings import DATA_DIR, CHANGE_REQUESTS_FILE


def ensure_change_requests_file():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not CHANGE_REQUESTS_FILE.exists():
        with CHANGE_REQUESTS_FILE.open("w", encoding="utf-8") as file:
            json.dump([], file, indent=4)


def load_change_requests():
    ensure_change_requests_file()

    with CHANGE_REQUESTS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_change_requests(requests):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with CHANGE_REQUESTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(requests, file, indent=4)


def create_change_request(title, request_text, priority="normal"):
    requests = load_change_requests()

    new_request = {
        "id": len(requests) + 1,
        "title": title.strip(),
        "request_text": request_text.strip(),
        "priority": priority.strip().lower(),
        "status": "open",
        "created_at": datetime.now(UTC).isoformat(),
    }

    requests.append(new_request)
    save_change_requests(requests)

    return new_request


def get_open_change_requests():
    requests = load_change_requests()
    return [item for item in requests if item["status"] == "open"]


def update_change_request_status(request_id, new_status):
    requests = load_change_requests()
    allowed_statuses = {"open", "approved", "closed"}

    if new_status not in allowed_statuses:
        return None

    for item in requests:
        if item["id"] == request_id:
            item["status"] = new_status
            save_change_requests(requests)
            return item

    return None