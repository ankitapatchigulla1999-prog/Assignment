"""Page Object for the Autocomplete Form (https://test.com/autocomplete-form)."""
from playwright.sync_api import Page, expect


class AutocompletePage:
    URL = "https://test.com/autocomplete-form"

    def __init__(self, page: Page):
        self.page = page
        self.input_field = page.locator("#input-field")
        self.suggestions = page.locator(".suggestions li")
        self.next_button = page.locator("#next-button")
        self.error_message = page.locator(".error-message")
        self.success_container = page.locator(".success-container")

    def goto(self):
        self.page.goto(self.URL)
        return self

    def type_text(self, text: str):
        self.input_field.fill(text)
        return self

    def visible_suggestions(self) -> list[str]:
        """Returns text of all currently visible (rendered) suggestion items."""
        return self.suggestions.all_text_contents()

    def click_suggestion(self, text: str):
        self.suggestions.filter(has_text=text).first.click()
        return self

    def click_next(self):
        self.next_button.click()
        return self

    def press_tab(self):
        self.page.keyboard.press("Tab")
        return self

    def press_enter(self):
        self.page.keyboard.press("Enter")
        return self

    def press_escape(self):
        self.page.keyboard.press("Escape")
        return self

    def expect_success(self):
        expect(self.success_container).to_be_visible()
        expect(self.error_message).to_be_hidden()
        return self

    def expect_error(self):
        expect(self.error_message).to_be_visible()
        return self

    def input_value(self) -> str:
        return self.input_field.input_value()
