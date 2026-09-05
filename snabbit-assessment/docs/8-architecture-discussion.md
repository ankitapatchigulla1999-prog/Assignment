# Architecture Discussion

## Framework Choice
Python + `pytest` + `pytest-playwright` for UI tests, and Python + `requests` + `pytest` for API
tests. This keeps a single language/toolchain across both suites, which simplifies CI setup and
matches common Python-based QA automation stacks.

## Design Pattern — Page Object Model (POM)
`AutocompletePage` (in `tests/ui/pages/`) encapsulates every locator and UI interaction for the
form (typing, clicking a suggestion, submitting, reading visible suggestions, keyboard actions).
Test files only call page-object methods and make assertions — they never touch a raw locator
directly. This means:
- If the form's DOM/selectors change, only `autocomplete_page.py` needs updating.
- Test intent stays readable (`form.click_suggestion(...)`, not raw CSS selectors scattered
  through every test).

## Separation of UI and API Suites
`tests/ui/` and `tests/api/` are kept fully independent — no shared fixtures beyond what pytest
loads per-directory. This mirrors how these suites would run in CI: UI tests need a real/headless
browser and are inherently slower; API tests are pure HTTP and can run in every commit's fast
feedback loop. Keeping them separate lets a pipeline run API tests on every push and UI tests on a
slower nightly/PR-gate schedule if needed.

## Config Isolation (`tests/ui/config/conftest.py`)
Browser context (locale `en-IN`, timezone `Asia/Kolkata`, viewport) is centralized in one fixture
so every UI test automatically runs under the same environment conditions specified in the
assignment (Chrome/Windows/English/India), rather than each test file re-specifying environment
setup.

## Known Gaps / Assumptions (flagged, not hidden)
- **Login is out of scope** per the assignment, so `logged_in_page` in `conftest.py` is a
  placeholder seam — in a real suite it would load a saved authenticated `storage_state.json` or
  call a login API helper before every test, rather than performing UI login per test (which would
  be slow and brittle).
- **API endpoint URLs are assumed**, since the assignment only specifies the FR-05 data contract,
  not real endpoint paths. `BASE_URL`/`SUBMIT_ENDPOINT` in the API tests are clearly marked
  placeholders to be swapped for the real environment's API base URL.
- Tests are written to be **runnable in structure and logic**, but since there is no live
  `test.com` environment or backend to execute against, they have not been run against a real
  server — see `README.md` for how to point them at a real environment.
