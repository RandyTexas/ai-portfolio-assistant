import ai_builder


def test_update_change_request_status_updates_existing_request(tmp_path, monkeypatch):
    test_file = tmp_path / "change_requests.json"

    monkeypatch.setattr(ai_builder, "CHANGE_REQUESTS_FILE", test_file)
    monkeypatch.setattr(ai_builder, "DATA_DIR", tmp_path)

    ai_builder.save_change_requests(
        [
            {
                "id": 1,
                "title": "Add cancel flow",
                "request_text": "Add a back option.",
                "priority": "high",
                "status": "open",
                "created_at": "2026-01-01T00:00:00+00:00",
            }
        ]
    )

    updated = ai_builder.update_change_request_status(1, "approved")
    requests = ai_builder.load_change_requests()

    assert updated is not None
    assert updated["status"] == "approved"
    assert requests[0]["status"] == "approved"


def test_update_change_request_status_rejects_bad_status(tmp_path, monkeypatch):
    test_file = tmp_path / "change_requests.json"

    monkeypatch.setattr(ai_builder, "CHANGE_REQUESTS_FILE", test_file)
    monkeypatch.setattr(ai_builder, "DATA_DIR", tmp_path)

    ai_builder.save_change_requests(
        [
            {
                "id": 1,
                "title": "Add cancel flow",
                "request_text": "Add a back option.",
                "priority": "high",
                "status": "open",
                "created_at": "2026-01-01T00:00:00+00:00",
            }
        ]
    )

    updated = ai_builder.update_change_request_status(1, "invalid_status")

    assert updated is None


def test_update_change_request_status_returns_none_for_missing_id(tmp_path, monkeypatch):
    test_file = tmp_path / "change_requests.json"

    monkeypatch.setattr(ai_builder, "CHANGE_REQUESTS_FILE", test_file)
    monkeypatch.setattr(ai_builder, "DATA_DIR", tmp_path)

    ai_builder.save_change_requests([])

    updated = ai_builder.update_change_request_status(99, "approved")

    assert updated is None