# Defect Identification — API Response vs. FR-05

## Actual Response (from Section 2)
```json
{
  "account_id": "98765",
  "account_email": "test123@gmail.com",
  "start_date": "2024-03-15T10:30:00Z",
  "end_date": "2024-03-15T10:32:00Z",
  "locale": "en",
  "text": "agile methodology",
  "suggestion_list": "agile methodology, agile methodology process, agile methodology process testing",
  "completed": "true"
}
```

## Discrepancies Found

### D1 — `start_date` / `end_date` are in UTC, not the user's local time (Critical)
FR-05 explicitly defines these fields as *"Timestamp in the user's local time when they reached/selected Next."*
The test environment specifies the user is in **India (IST, UTC+05:30)**. Both timestamps carry a
`Z` suffix, which denotes **UTC**, not IST. Per the contract, `start_date` should read
`2024-03-15T16:00:00+05:30` (10:30 UTC + 5:30), not `2024-03-15T10:30:00Z`.
**Impact:** Any reporting, SLA, or audit logic keyed off "local time" will be silently 5.5 hours off for every Indian user.

### D2 — `locale` is `"en"`, not a full IETF BCP 47 tag (High)
FR-05 requires *"IETF BCP 47 format of the user's locale (e.g., en-IN)."* A bare `"en"` is a valid
**language** subtag but is not a complete locale identifier for a user in India — it drops the
required **region** subtag. Expected value: `"en-IN"`.
**Impact:** Any downstream locale-aware formatting (dates, currency, number formats) driven by this field will default to a generic English locale instead of India-specific formatting.

### D3 — `completed` is a string `"true"`, not a JSON boolean (High)
FR-05 explicitly types this field as *"Boolean representing the status of form response upload."*
The response returns the **string** `"true"` (quoted), not the JSON literal `true`. This is a strict
data-type contract violation, not a formatting nitpick.
**Impact:** Any consumer doing a strict boolean check (`if completed:` in a strongly-typed system, or `completed === true` in JS) will evaluate this incorrectly depending on the language/parser, and schema validators will reject the payload outright.

### D4 — `suggestion_list` content is ambiguous against the spec wording (Medium — flagged, not confirmed defect)
FR-05 describes this field as *"Comma-separated string of suggestions **matching the value entered/selected**."*
The user selected `"agile methodology"` by **clicking** the first list item (no typing occurred), so
technically no filter was ever applied — all three suggestions were visible pre-click under the
default prefix-match rule (all three genuinely start with "agile methodology"). Under a strict
reading of FR-02, returning all three is **arguably correct**. However, the phrasing "matching the
value entered/selected" could also be read to mean *only* the suggestions that match the **final**
selected value re-evaluated against the filter — which, in this case, still yields all three, since
each candidate string begins with "agile methodology."
**Recommendation:** Not a confirmed defect under current rules, but the requirement should be
clarified with the product owner, and a dedicated test case (see `4-test-cases.md`, TC-07) should
lock in the expected behavior explicitly so this doesn't silently change on a future refactor.

### D5 — `account_id` returned as a string, not a numeric type (Low — observation only)
FR-05 only describes this field as *"ID of the user account"* without specifying a type. Returning
it as a string (`"98765"`) is a common and often intentional practice (avoids precision-loss issues
in JS, keeps IDs opaque). **Not flagged as a defect**, but noted here since it's a deviation from an
implicit assumption that IDs are numeric — worth a one-line confirmation from the API team that this
is intentional rather than accidental.

## Summary Table

| ID | Field | Severity | Confirmed Defect? |
|----|-------|----------|--------------------|
| D1 | start_date / end_date | Critical | Yes |
| D2 | locale | High | Yes |
| D3 | completed | High | Yes |
| D4 | suggestion_list | Medium | Ambiguous — needs clarification |
| D5 | account_id | Low | No — observation only |
