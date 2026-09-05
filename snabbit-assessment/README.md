# Autocomplete Form — QA Assessment Submission

## What's in here
- `docs/1-requirement-analysis.md` — requirement breakdown and open questions
- `docs/2-test-scenarios.md` — top 10 risk-ranked test scenarios
- `docs/3-defect-identification.md` — API response vs. FR-05 discrepancy analysis
- `docs/4-test-cases.md` — 12 detailed test cases (UI + API)
- `docs/7-ai-reflection.md` — AI usage disclosure (assignment Task 6)
- `docs/8-architecture-discussion.md` — framework/design rationale and known assumptions
- `tests/ui/` — Playwright UI automation (Page Object Model)
- `tests/api/` — API contract/schema automation

## Prerequisites
- Python 3.10+
- pip

## Setup
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

## Running the tests

Run everything:
```bash
pytest
```

Run only UI tests:
```bash
pytest tests/ui
```

Run only API tests:
```bash
pytest tests/api
```

Run with a visible (headed) browser for debugging:
```bash
pytest tests/ui --headed
```

## Important assumptions (read before running against a real environment)
1. **`https://test.com` is a placeholder domain** from the assignment brief — it does not resolve
   to a real server. To run these tests against an actual environment, update:
   - `AutocompletePage.URL` in `tests/ui/pages/autocomplete_page.py`
   - `BASE_URL` in `tests/api/tests/test_form_submission_api.py`
2. **Login is out of scope** per the assignment. `logged_in_page` in
   `tests/ui/config/conftest.py` is a placeholder fixture — wire it up to your real auth
   mechanism (storage state or API login) before running UI tests end-to-end.
3. **API endpoint paths are assumed** (e.g., `/api/autocomplete-form/submit`,
   `/api/responses/{id}`), since the assignment specifies only the data contract (FR-05), not
   the actual routes. Update these once the real API surface is available.

## AI usage disclosure
Per the assignment's AI usage policy, `docs/7-ai-reflection.md` documents which AI tool was used,
what it was used for, and specific examples of corrections made to its output. The prompt file(s)
and full conversation transcript should be exported from the AI tool and included alongside this
submission as required.
