# AI Reflection

## a. Tools Used
Claude (Anthropic), used conversationally within the Claude.ai chat interface, including its
code-execution/file-creation environment.

## b. Usage Areas
- Structuring the repository per the required submission layout.
- Drafting the initial requirement analysis and identifying ambiguities in the spec.
- Generating a first pass of the top-10 risk-ranked test scenarios.
- Generating the initial API response vs. FR-05 discrepancy analysis.
- Drafting detailed test cases (UI and API).
- Writing the initial Page Object class, Playwright UI test scripts, and API contract test scripts.
- Drafting this reflection document itself.

## c. Modifications Made (minimum 2 examples)

1. **Corrected an over-confident defect claim on `suggestion_list` (D4).**
   The first AI draft flagged the `suggestion_list` field in the Section 2 API response as a
   confirmed defect, reasoning that "only the selected suggestion should appear." On closer
   reading of FR-02 (prefix match is the *default*, always-on rule) and the fact that all three
   sample suggestions genuinely share the prefix "agile methodology," I corrected this to an
   **ambiguous / needs-clarification** item rather than a confirmed defect, and added TC-07 to
   lock in the agreed behavior explicitly. Overstating a defect here would have sent a wrong
   signal to the engineering team about the filtering logic actually being broken.

2. **Fixed a scope/URL assumption in the API tests.**
   The initial API test draft called a guessed endpoint path without flagging it as an assumption.
   Since the assignment only specifies the **data contract** (FR-05), not the actual REST endpoint
   URLs, I added an explicit note (see `README.md`, "Assumptions") that `BASE_URL` /
   `SUBMIT_ENDPOINT` are placeholders that must be swapped for the real API base URL before the
   suite can run against a live environment — rather than letting the tests imply a working,
   verified endpoint that was never actually confirmed.

3. **Tightened the local-timestamp regex.**
   The first version of `LOCAL_TS_PATTERN` in the API tests accepted a trailing `Z` as well as a
   numeric offset, which would have made the "not UTC" assertion in
   `test_timestamps_are_in_local_time_not_utc` pass even for a UTC timestamp in some edge cases. I
   tightened the pattern to require an explicit `+HH:MM`/`-HH:MM` offset and added a separate,
   explicit `assert not value.endswith("Z")` check so the test fails loudly and specifically on
   the exact defect (D1) rather than a vague schema mismatch.

## d. AI Limitations (minimum 1 example)
The AI's first pass at the risk-ranking (Section 1 of the scenario list) initially ranked
**keyboard/tab navigation** above the **data-contract validation** scenario. This under-weighted
the fact that a silent data-integrity bug (wrong timestamps, wrong boolean type) reaching
production has a far larger blast radius than an accessibility/keyboard bug, even though the
keyboard bug is more immediately visible during manual testing. This was corrected manually by
re-ordering the list so that scenarios with **silent, undetected production impact** are ranked
above scenarios that are merely **inconvenient but visible**. This reflects a general limitation:
without explicit business-impact framing, the AI tends to rank "obviously testable UI behavior"
above "quietly dangerous backend/data correctness" issues, when the latter is usually higher real-world risk in production systems.
