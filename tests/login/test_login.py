"""
Login module tests - run against https://www.saucedemo.com
"""

from conftest import attach_context

BASE_URL = "https://www.saucedemo.com"


def test_valid_login(page):
    page.goto(BASE_URL)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    page.wait_for_selector(".inventory_list")
    assert "inventory.html" in page.url


def test_invalid_credentials(page, request):
    page.goto(BASE_URL)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "wrong_password")
    page.click("#login-button")
    error = page.locator("[data-test='error']").inner_text()
    attach_context(request, visible_error_text=error)
    assert "do not match" in error.lower() or "epic sadface" in error.lower()


def test_locked_out_user_brute_force_lockout(page, request):
    page.goto(BASE_URL)
    page.fill("#user-name", "locked_out_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    error = page.locator("[data-test='error']").inner_text()
    attach_context(request, visible_error_text=error)
    assert "locked out" in error.lower()


def test_session_expiry_redirects_to_login(page, request):
    page.goto(BASE_URL)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    page.wait_for_selector(".inventory_list")

    page.context.clear_cookies()
    page.goto(f"{BASE_URL}/inventory.html")
    attach_context(request, page_url_after_clear=page.url)
    assert "inventory.html" not in page.url or page.locator("[data-test='error']").count() > 0


def test_deliberate_failure_for_explainer_demo(page):
    """Intentionally-failing test to produce a real, non-mocked sample
    output for Task 3's 'sample output' requirement. EXPECTED to fail -
    check reports/failure_explanations.json after running pytest."""
    page.goto(BASE_URL)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    assert page.locator("#nonexistent-widget-xyz").is_visible(timeout=2000)