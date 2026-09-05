"""
API tests for the Autocomplete Form submission endpoint, validating the FR-05
data contract: schema shape, field types, BCP-47 locale format, and correct
suggestion_list filtering. Includes negative test cases for malformed payloads.
"""
import re
import pytest
import requests

BASE_URL = "https://test.com/api"
SUBMIT_ENDPOINT = f"{BASE_URL}/autocomplete-form/submit"

REQUIRED_FIELDS = {
    "account_id": str,
    "account_email": str,
    "start_date": str,
    "end_date": str,
    "locale": str,
    "text": str,
    "suggestion_list": str,
    "completed": bool,
}

BCP47_PATTERN = re.compile(r"^[a-z]{2,3}(-[A-Z]{2})?$")
# ISO-8601 timestamp with an explicit numeric UTC offset, e.g. +05:30 (not bare Z/UTC).
LOCAL_TS_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$")


@pytest.fixture
def valid_submission_payload():
    return {
        "account_id": "98765",
        "account_email": "test123@gmail.com",
        "text": "agile methodology",
        "suggestion_list": "agile methodology, agile methodology process, agile methodology process testing",
    }


def _get_form_response(session_id: str = "98765"):
    """Helper: GET the persisted record for the submitted form response."""
    return requests.get(f"{BASE_URL}/responses/{session_id}")


class TestSchemaContract:
    def test_response_contains_all_required_fields(self, valid_submission_payload):
        resp = _get_form_response()
        body = resp.json()
        for field in REQUIRED_FIELDS:
            assert field in body, f"Missing required field: {field}"

    def test_response_has_no_unexpected_extra_fields(self):
        resp = _get_form_response()
        body = resp.json()
        extra = set(body.keys()) - set(REQUIRED_FIELDS.keys())
        assert not extra, f"Unexpected extra fields in response: {extra}"


class TestFieldTypes:
    def test_completed_is_boolean_not_string(self):
        resp = _get_form_response()
        body = resp.json()
        assert isinstance(body["completed"], bool), (
            f"Expected boolean for 'completed', got {type(body['completed'])} "
            f"with value {body['completed']!r}"
        )

    def test_timestamps_are_in_local_time_not_utc(self):
        resp = _get_form_response()
        body = resp.json()
        for field in ("start_date", "end_date"):
            value = body[field]
            assert not value.endswith("Z"), (
                f"{field} is in UTC ('Z' suffix) but FR-05 requires local time (IST, +05:30)"
            )
            assert LOCAL_TS_PATTERN.match(value), (
                f"{field} value {value!r} is not a local ISO-8601 timestamp with offset"
            )

    def test_locale_matches_bcp47_with_region(self):
        resp = _get_form_response()
        body = resp.json()
        locale = body["locale"]
        assert BCP47_PATTERN.match(locale), f"Locale {locale!r} is not valid BCP-47"
        assert "-" in locale, (
            f"Locale {locale!r} is missing the region subtag (expected e.g. 'en-IN')"
        )


class TestSuggestionListFiltering:
    def test_suggestion_list_contains_only_matching_suggestions(self):
        """FR-05 + FR-02: suggestion_list must reflect suggestions that genuinely
        match the submitted text under the active filter mode, not the full
        static list regardless of relevance."""
        resp = _get_form_response()
        body = resp.json()
        submitted_text = body["text"]
        suggestions = [s.strip() for s in body["suggestion_list"].split(",")]
        for s in suggestions:
            assert s.startswith(submitted_text) or submitted_text in s, (
                f"Suggestion {s!r} does not match submitted text {submitted_text!r} "
                f"under either prefix or substring rules"
            )


class TestNegativeCases:
    def test_missing_required_field_is_rejected(self, valid_submission_payload):
        payload = dict(valid_submission_payload)
        payload.pop("account_email")
        resp = requests.post(SUBMIT_ENDPOINT, json=payload)
        assert resp.status_code == 400, (
            f"Expected 400 for missing 'account_email', got {resp.status_code}"
        )

    def test_invalid_completed_type_is_rejected(self, valid_submission_payload):
        payload = dict(valid_submission_payload)
        payload["completed"] = "yes"  # invalid: should be boolean, not arbitrary string
        resp = requests.post(SUBMIT_ENDPOINT, json=payload)
        assert resp.status_code == 400, (
            f"Expected 400 for invalid 'completed' type, got {resp.status_code}"
        )

    def test_malformed_locale_is_rejected(self, valid_submission_payload):
        payload = dict(valid_submission_payload)
        payload["locale"] = "not-a-locale!!"
        resp = requests.post(SUBMIT_ENDPOINT, json=payload)
        assert resp.status_code == 400, (
            f"Expected 400 for malformed locale, got {resp.status_code}"
        )
