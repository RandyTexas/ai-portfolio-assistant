import ai_builder


def test_create_change_request_saves_request(tmp_path, monkeypatch):
    test_file = tmp_path / "change_requests.json"

    monkeypatch.setattr(ai_builder, "CHANGE_REQUESTS_FILE", test_file)
    monkeypatch.setattr(ai_builder, "DATA_DIR", tmp_path)

    new_request = ai_builder.create_change_request(
        title="Add cancel flow",
        request_text="Add a back or cancel option to menu inputs.",
        priority="high",
    )

    requests = ai_builder.load_change_requests()

    assert new_request["id"] == 1
    assert new_request["title"] == "Add cancel flow"
    assert new_request["priority"] == "high"
    assert new_request["status"] == "open"
    assert len(requests) == 1


def test_load_change_requests_starts_empty(tmp_path, monkeypatch):
    test_file = tmp_path / "change_requests.json"

    monkeypatch.setattr(ai_builder, "CHANGE_REQUESTS_FILE", test_file)
    monkeypatch.setattr(ai_builder, "DATA_DIR", tmp_path)

    requests = ai_builder.load_change_requests()

    assert requests == []


def test_get_open_change_requests_filters_closed_items(tmp_path, monkeypatch):
    test_file = tmp_path / "change_requests.json"

    monkeypatch.setattr(ai_builder, "CHANGE_REQUESTS_FILE", test_file)
    monkeypatch.setattr(ai_builder, "DATA_DIR", tmp_path)

    ai_builder.save_change_requests(
        [
            {
                "id": 1,
                "title": "Open request",
                "request_text": "Do something",
                "priority": "normal",
                "status": "open",
                "created_at": "2026-01-01T00:00:00+00:00",
            },
            {
                "id": 2,
                "title": "Closed request",
                "request_text": "Done already",
                "priority": "low",
                "status": "closed",
                "created_at": "2026-01-01T00:00:00+00:00",
            },
        ]
    )

    open_requests = ai_builder.get_open_change_requests()

    assert len(open_requests) == 1
    assert open_requests[0]["title"] == "Open request"
    assert open_requests[0]["status"] == "open"


def test_get_approved_change_requests_filters_approved_items(tmp_path, monkeypatch):
    test_file = tmp_path / "change_requests.json"

    monkeypatch.setattr(ai_builder, "CHANGE_REQUESTS_FILE", test_file)
    monkeypatch.setattr(ai_builder, "DATA_DIR", tmp_path)

    ai_builder.save_change_requests(
        [
            {
                "id": 1,
                "title": "Approved request",
                "request_text": "Implement something",
                "priority": "high",
                "status": "approved",
                "created_at": "2026-01-01T00:00:00+00:00",
            },
            {
                "id": 2,
                "title": "Open request",
                "request_text": "Still waiting",
                "priority": "normal",
                "status": "open",
                "created_at": "2026-01-01T00:00:00+00:00",
            },
        ]
    )

    approved_requests = ai_builder.get_approved_change_requests()

    assert len(approved_requests) == 1
    assert approved_requests[0]["title"] == "Approved request"
    assert approved_requests[0]["status"] == "approved"