import json
from datetime import datetime, UTC

from config.settings import DATA_DIR, IMPLEMENTATION_QUEUE_FILE
from ai_builder import load_change_requests


def ensure_implementation_queue_file():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not IMPLEMENTATION_QUEUE_FILE.exists():
        with IMPLEMENTATION_QUEUE_FILE.open("w", encoding="utf-8") as file:
            json.dump([], file, indent=4)


def load_implementation_queue():
    ensure_implementation_queue_file()

    with IMPLEMENTATION_QUEUE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_implementation_queue(queue_items):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with IMPLEMENTATION_QUEUE_FILE.open("w", encoding="utf-8") as file:
        json.dump(queue_items, file, indent=4)


def add_approved_request_to_queue(request_id):
    requests = load_change_requests()
    queue_items = load_implementation_queue()

    for request in requests:
        if request["id"] == request_id:
            if request["status"] != "approved":
                return None

            already_queued = any(item["request_id"] == request_id for item in queue_items)
            if already_queued:
                return None

            queue_item = {
                "queue_id": len(queue_items) + 1,
                "request_id": request["id"],
                "title": request["title"],
                "request_text": request["request_text"],
                "priority": request["priority"],
                "source_status": request["status"],
                "queue_status": "ready",
                "queued_at": datetime.now(UTC).isoformat(),
            }

            queue_items.append(queue_item)
            save_implementation_queue(queue_items)
            return queue_item

    return None


def update_queue_item_status(queue_id, new_status):
    queue_items = load_implementation_queue()
    allowed_statuses = {"ready", "in_progress", "completed"}

    if new_status not in allowed_statuses:
        return None

    for item in queue_items:
        if item["queue_id"] == queue_id:
            item["queue_status"] = new_status
            save_implementation_queue(queue_items)
            return item

    return None