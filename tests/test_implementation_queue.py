import ai_builder
import implementation_queue


def test_add_approved_request_to_queue_adds_ready_item(tmp_path, monkeypatch):
    change_requests_file = tmp_path / "change_requests.json"
    implementation_queue_file = tmp_path / "implementation_queue.json"

    monkeypatch.setattr(ai_builder, "CHANGE_REQUESTS_FILE", change_requests_file)
    monkeypatch.setattr(ai_builder, "DATA_DIR", tmp_path)

    monkeypatch.setattr(implementation_queue, "IMPLEMENTATION_QUEUE_FILE", implementation_queue_file)
    monkeypatch.setattr(implementation_queue, "DATA_DIR", tmp_path)

    ai_builder.save_change_requests(
        [
            {
                "id": 1,
                "title": "Add cancel flow",
                "request_text": "Add a cancel option to form inputs.",
                "priority": "high",
                "status": "approved",
                "created_at": "2026-01-01T00:00:00+00:00",
            }
        ]
    )

    queue_item = implementation_queue.add_approved_request_to_queue(1)
    queue_items = implementation_queue.load_implementation_queue()

    assert queue_item is not None
    assert queue_item["request_id"] == 1
    assert queue_item["title"] == "Add cancel flow"
    assert queue_item["queue_status"] == "ready"
    assert len(queue_items) == 1


def test_add_approved_request_to_queue_rejects_non_approved_request(tmp_path, monkeypatch):
    change_requests_file = tmp_path / "change_requests.json"
    implementation_queue_file = tmp_path / "implementation_queue.json"

    monkeypatch.setattr(ai_builder, "CHANGE_REQUESTS_FILE", change_requests_file)
    monkeypatch.setattr(ai_builder, "DATA_DIR", tmp_path)

    monkeypatch.setattr(implementation_queue, "IMPLEMENTATION_QUEUE_FILE", implementation_queue_file)
    monkeypatch.setattr(implementation_queue, "DATA_DIR", tmp_path)

    ai_builder.save_change_requests(
        [
            {
                "id": 1,
                "title": "Open request",
                "request_text": "Still being reviewed.",
                "priority": "normal",
                "status": "open",
                "created_at": "2026-01-01T00:00:00+00:00",
            }
        ]
    )

    queue_item = implementation_queue.add_approved_request_to_queue(1)
    queue_items = implementation_queue.load_implementation_queue()

    assert queue_item is None
    assert queue_items == []


def test_add_approved_request_to_queue_rejects_duplicate_queueing(tmp_path, monkeypatch):
    change_requests_file = tmp_path / "change_requests.json"
    implementation_queue_file = tmp_path / "implementation_queue.json"

    monkeypatch.setattr(ai_builder, "CHANGE_REQUESTS_FILE", change_requests_file)
    monkeypatch.setattr(ai_builder, "DATA_DIR", tmp_path)

    monkeypatch.setattr(implementation_queue, "IMPLEMENTATION_QUEUE_FILE", implementation_queue_file)
    monkeypatch.setattr(implementation_queue, "DATA_DIR", tmp_path)

    ai_builder.save_change_requests(
        [
            {
                "id": 1,
                "title": "Approved request",
                "request_text": "Queue this only once.",
                "priority": "high",
                "status": "approved",
                "created_at": "2026-01-01T00:00:00+00:00",
            }
        ]
    )

    first_item = implementation_queue.add_approved_request_to_queue(1)
    second_item = implementation_queue.add_approved_request_to_queue(1)
    queue_items = implementation_queue.load_implementation_queue()

    assert first_item is not None
    assert second_item is None
    assert len(queue_items) == 1


def test_load_implementation_queue_starts_empty(tmp_path, monkeypatch):
    implementation_queue_file = tmp_path / "implementation_queue.json"

    monkeypatch.setattr(implementation_queue, "IMPLEMENTATION_QUEUE_FILE", implementation_queue_file)
    monkeypatch.setattr(implementation_queue, "DATA_DIR", tmp_path)

    queue_items = implementation_queue.load_implementation_queue()

    assert queue_items == []
    