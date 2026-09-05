# Requirement Analysis — Autocomplete Form

## Feature Summary
An Autocomplete form (`/autocomplete-form`) presents a text input backed by a suggestion list.
Users either type free text or select a suggestion, then submit via **Next**, which fires a
REST call to persist a response record.

## Key Behaviors Identified

| Requirement | Behavior |
|--- |---|
| FR-01 | Input accepts free text AND click/tap selection from suggestions — two independent input paths that must both lead to a valid submission. |
| FR-02 | Default filtering = **prefix match**. Suggestions whose *start* doesn't match typed text are removed from the DOM/visible list. |
| FR-03 | Configurable **substring match** mode — suggestions remain if the typed text appears *anywhere* in the suggestion. This is a backend-configured toggle, not user-facing, so tests must be data-driven per config state. |
| FR-04 | Submission is API-backed. Success = HTTP 200 + success message. Failure = error message. Implies the UI must handle both response paths and a network/error state isn't explicitly defined (ambiguity, see below). |
| FR-05 | Defines the exact persisted data contract — 8 required fields with explicit types/formats (boolean, IETF BCP 47 locale, comma-separated string, local timestamp). |

## Ambiguities / Open Questions (worth flagging to the team)
1. **FR-04** does not define behavior for network failure / timeout (distinct from "invalid input" error) — is the same `.error-message` shown, or is there a separate state?
2. **FR-05** does not explicitly state whether `suggestion_list` reflects the suggestions **visible at the moment of selection** or **only the final selected value**. This directly affects the expected value in the Section 2 API response and is addressed in `3-defect-identification.md`.
3. The HTML has a single shared `.error-message` / `.success-container`, but there's no explicit spec for what triggers "invalid input" on the client vs. server side (e.g., is a free-typed value that doesn't match any suggestion allowed to submit at all, or blocked before the API call?).
4. No explicit max-length, empty-input, or special-character handling is defined for the text field.
5. Locale requirement (`en-IN` style) implies the backend must resolve the user's full locale (language **and** region) — but the login/environment details only confirm browser language, not explicit region.

These ambiguities are treated as **testable risk areas** in the scenario list rather than skipped, since the assessment prompt is deliberately terse in these places.
