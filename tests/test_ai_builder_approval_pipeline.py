import ai_builder


def test_get_approved_change_requests_returns_only_approved(tmp_path, monkeypatch):
    test_file = tmp_path / "change_requests.json"

    monkeypatch.setattr(ai_builder, "CHANGE_REQUESTS_FILE", test_file)
    monkeypatch.setattr(ai_builder, "DATA_DIR", tmp_path)

    ai_builder.save_change_requests(
        [
            {
                "id": 1,
                "title": "Approved request",
                "request_text": "Implement this",
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
            {
                "id": 3,
                "title": "Closed request",
                "request_text": "Done already",
                "priority": "low",
                "status": "closed",
                "created_at": "2026-01-01T00:00:00+00:00",
            },
        ]
    )

    approved_requests = ai_builder.get_approved_change_requests()

    assert len(approved_requests) == 1
    assert approved_requests[0]["id"] == 1
    assert approved_requests[0]["title"] == "Approved request"
    assert approved_requests[0]["status"] == "approved"


def test_request_can_move_from_open_to_approved(tmp_path, monkeypatch):
    test_file = tmp_path / "change_requests.json"

    monkeypatch.setattr(ai_builder, "CHANGE_REQUESTS_FILE", test_file)
    monkeypatch.setattr(ai_builder, "DATA_DIR", tmp_path)

    ai_builder.save_change_requests(
        [
            {
                "id": 1,
                "title": "Add AI patch mode",
                "request_text": "Turn approved requests into implementation queue items.",
                "priority": "high",
                "status": "open",
                "created_at": "2026-01-01T00:00:00+00:00",
            }
        ]
    )

    updated = ai_builder.update_change_request_status(1, "approved")
    approved_requests = ai_builder.get_approved_change_requests()

    assert updated is not None
    assert updated["status"] == "approved"
    assert len(approved_requests) == 1
    assert approved_requests[0]["id"] == 1


def test_closed_requests_do_not_show_in_approved_list(tmp_path, monkeypatch):
    test_file = tmp_path / "change_requests.json"

    monkeypatch.setattr(ai_builder, "CHANGE_REQUESTS_FILE", test_file)
    monkeypatch.setattr(ai_builder, "DATA_DIR", tmp_path)

    ai_builder.save_change_requests(
        [
            {
                "id": 1,
                "title": "Closed request",
                "request_text": "Not needed",
                "priority": "low",
                "status": "closed",
                "created_at": "2026-01-01T00:00:00+00:00",
            }
        ]
    )

    approved_requests = ai_builder.get_approved_change_requests()

    assert approved_requests == []