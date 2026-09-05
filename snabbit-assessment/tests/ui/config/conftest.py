"""Shared pytest-playwright fixtures and environment/browser configuration."""
import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Match the specified test environment: Chrome on Windows 10, English, India locale/timezone."""
    return {
        **browser_context_args,
        "locale": "en-IN",
        "timezone_id": "Asia/Kolkata",
        "viewport": {"width": 1366, "height": 768},
    }


@pytest.fixture
def logged_in_page(page):
    """
    Assumes login is out of scope per the assignment brief; this fixture is a seam
    for injecting an authenticated session (e.g., via storage_state or an API login
    call) once the real login endpoint/mechanism is available.
    """
    # Placeholder: in a real suite this would call an auth helper or load a saved
    # storage_state.json for test123@gmail.com before navigating to the form.
    yield page
