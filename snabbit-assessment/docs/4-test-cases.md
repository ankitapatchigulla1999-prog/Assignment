# Detailed Test Cases

---
### TC-01 — Prefix-match filtering removes non-matching suggestions
**Preconditions:** User logged in as `test123@gmail.com`; on `/autocomplete-form`; backend filter mode = default (prefix match).
**Test Steps:**
1. Navigate to the Autocomplete form.
2. Click the text input field.
3. Type `xyz`.
**Expected Results:** All three suggestions (`agile methodology`, `agile methodology process`, `agile methodology process testing`) disappear from the visible list, since none start with "xyz".
**Test Data:** Input text: `xyz`

---
### TC-02 — Prefix-match filtering keeps matching suggestions
**Preconditions:** Same as TC-01.
**Test Steps:**
1. Navigate to the Autocomplete form.
2. Type `agile met` into the input field.
**Expected Results:** All three suggestions remain visible (all three start with "agile met...").
**Test Data:** Input text: `agile met`

---
### TC-03 — Match-Anywhere mode surfaces mid-string matches
**Preconditions:** Backend config set to Match-Anywhere (FR-03) mode.
**Test Steps:**
1. Navigate to the Autocomplete form.
2. Type `method` into the input field.
**Expected Results:** All three suggestions remain visible, since "method" appears inside each of them even though none start with it.
**Test Data:** Input text: `method`

---
### TC-04 — Selecting a suggestion via click populates the input field exactly
**Preconditions:** Form loaded, suggestion list visible and unfiltered.
**Test Steps:**
1. Click the second suggestion, `agile methodology process`.
**Expected Results:** The input field value becomes exactly `agile methodology process` (no leading/trailing whitespace, no truncation).
**Test Data:** N/A (click-based selection)

---
### TC-05 — Successful submission shows success message and returns HTTP 200
**Preconditions:** Form loaded; a valid suggestion has been selected.
**Test Steps:**
1. Click suggestion `agile methodology`.
2. Click the **Next** button.
**Expected Results:** The REST call returns HTTP 200; `.success-container` becomes visible with the text "Success! Your response has been recorded."; `.error-message` remains hidden.
**Test Data:** Selected suggestion: `agile methodology`

---
### TC-06 — Invalid input on submission shows error and does not falsely mark completion
**Preconditions:** Form loaded.
**Test Steps:**
1. Type free text that matches no suggestion, e.g., `random unrelated text`.
2. Click **Next** without selecting a suggestion from the list.
**Expected Results:** `.error-message` becomes visible with text "Error: Invalid input. Please select a valid suggestion."; no record is persisted with `completed: true` for this attempt (verified via API check).
**Test Data:** Input text: `random unrelated text`

---
### TC-07 — [API] `suggestion_list` reflects only the suggestions valid at time of selection
**Preconditions:** Backend in default prefix-match mode; user selects `agile methodology` via click with no prior typing.
**Test Steps:**
1. Perform the UI flow: click suggestion `agile methodology`, click **Next**.
2. GET the persisted response record via the API.
**Expected Results:** `suggestion_list` equals `"agile methodology, agile methodology process, agile methodology process testing"` (all three, since all begin with the selected text under prefix rules). This test locks in the D4 ambiguity as an explicit, agreed behavior.
**Test Data:** N/A — see `3-defect-identification.md` D4 for rationale.

---
### TC-08 — [API] Response schema and field types match the FR-05 data contract
**Preconditions:** A form submission has just completed successfully.
**Test Steps:**
1. GET the persisted response record via the API.
2. Validate the JSON against the FR-05 schema (all 8 fields present, correct types).
**Expected Results:**
   - `completed` is JSON boolean `true`, not the string `"true"`.
   - `start_date` / `end_date` are ISO-8601 timestamps with a `+05:30` offset (IST), not `Z` (UTC).
   - `locale` matches full BCP-47 pattern with region, e.g. `en-IN`, not bare `en`.
   - All 8 required fields (`account_id`, `account_email`, `start_date`, `end_date`, `locale`, `text`, `suggestion_list`, `completed`) are present with no extras.
**Test Data:** N/A — validated against the live/mock API response.

---
### TC-09 — [API] Missing required field returns a validation error, not a silent 200
**Preconditions:** API test harness can send a raw malformed POST payload.
**Test Steps:**
1. Send a POST request to the form-submission endpoint with the `locale` field omitted.
**Expected Results:** API responds with a 4xx error (e.g., 400) and a descriptive validation message; no record is persisted.
**Test Data:** Payload missing `locale`.

---
### TC-10 — [API] Invalid data type in a field is rejected
**Preconditions:** Same as TC-09.
**Test Steps:**
1. Send a POST request where `completed` is sent as the string `"yes"` instead of a boolean.
**Expected Results:** API responds with a 4xx validation error rather than accepting and coercing the value.
**Test Data:** Payload with `"completed": "yes"`.

---
### TC-11 — Tab-key navigation follows logical focus order
**Preconditions:** Form loaded, focus on page body.
**Test Steps:**
1. Press **Tab** repeatedly from the top of the form.
**Expected Results:** Focus order is: text input → suggestion list item(s) → Next button, with no focus trap or skipped elements.
**Test Data:** N/A

---
### TC-12 — Escape key clears/closes the active suggestion interaction
**Preconditions:** Input field focused with suggestions visible.
**Test Steps:**
1. Type `agile` (suggestions filter/remain visible).
2. Press **Escape**.
**Expected Results:** Suggestion list closes/collapses (exact behavior — clear input vs. just close list — should be confirmed with product; test asserts list is no longer visible).
**Test Data:** Input text: `agile`
