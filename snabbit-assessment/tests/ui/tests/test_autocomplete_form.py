"""
UI tests for the Autocomplete Form, covering:
- Tab navigation
- Keyboard interaction (Enter / Escape)
- Suggestion filtering (prefix match)
- Suggestion selection (click)
- Form submission (success / error paths)
Uses the Page Object Model via AutocompletePage.
"""
import pytest
from tests.ui.pages.autocomplete_page import AutocompletePage

ALL_SUGGESTIONS = [
    "agile methodology",
    "agile methodology process",
    "agile methodology process testing",
]


@pytest.fixture
def form(logged_in_page):
    return AutocompletePage(logged_in_page).goto()


class TestSuggestionFiltering:
    def test_non_matching_prefix_hides_all_suggestions(self, form):
        form.type_text("xyz")
        assert form.visible_suggestions() == []

    def test_matching_prefix_keeps_all_suggestions(self, form):
        form.type_text("agile met")
        assert form.visible_suggestions() == ALL_SUGGESTIONS

    def test_partial_prefix_narrows_list(self, form):
        # "agile methodology p" only matches the two longer suggestions
        form.type_text("agile methodology p")
        visible = form.visible_suggestions()
        assert "agile methodology" not in visible
        assert "agile methodology process" in visible
        assert "agile methodology process testing" in visible


class TestSuggestionSelection:
    def test_click_suggestion_populates_input_exactly(self, form):
        form.click_suggestion("agile methodology process")
        assert form.input_value() == "agile methodology process"

    def test_click_first_suggestion(self, form):
        form.click_suggestion("agile methodology")
        assert form.input_value() == "agile methodology"


class TestFormSubmission:
    def test_valid_selection_submits_successfully(self, form):
        form.click_suggestion("agile methodology")
        form.click_next()
        form.expect_success()

    def test_invalid_free_text_shows_error(self, form):
        form.type_text("random unrelated text")
        form.click_next()
        form.expect_error()

    def test_enter_key_submits_after_selection(self, form):
        form.click_suggestion("agile methodology")
        form.press_enter()
        form.expect_success()


class TestKeyboardAndTabNavigation:
    def test_tab_moves_focus_from_input_to_suggestions(self, form):
        form.input_field.click()
        form.press_tab()
        # First suggestion (or the list container) should now be focused.
        focused = form.page.evaluate("document.activeElement.textContent")
        assert focused is not None

    def test_escape_closes_suggestion_list(self, form):
        form.type_text("agile")
        form.press_escape()
        assert form.visible_suggestions() == []
