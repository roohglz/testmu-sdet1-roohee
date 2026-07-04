"""
Dashboard module tests - run against saucedemo.com's inventory page,
used here as our stand-in "dashboard" (widget grid = product cards).
"""

BASE_URL = "https://www.saucedemo.com"


def _login(page, username="standard_user", password="secret_sauce"):
    page.goto(BASE_URL)
    page.fill("#user-name", username)
    page.fill("#password", password)
    page.click("#login-button")


def test_widgets_load_with_expected_count(page):
    _login(page)
    page.wait_for_selector(".inventory_item")
    items = page.locator(".inventory_item")
    assert items.count() == 6


def test_data_accuracy_each_item_has_name_and_price(page):
    _login(page)
    page.wait_for_selector(".inventory_item")
    items = page.locator(".inventory_item")
    for i in range(items.count()):
        item = items.nth(i)
        assert item.locator(".inventory_item_name").inner_text().strip() != ""
        price_text = item.locator(".inventory_item_price").inner_text()
        assert price_text.startswith("$")


def test_sort_by_price_low_to_high(page):
    _login(page)
    page.wait_for_selector(".inventory_item")
    page.select_option(".product_sort_container", "lohi")
    prices = page.locator(".inventory_item_price").all_inner_texts()
    numeric_prices = [float(p.replace("$", "")) for p in prices]
    assert numeric_prices == sorted(numeric_prices)


def test_sort_by_name_z_to_a(page):
    _login(page)
    page.wait_for_selector(".inventory_item")
    page.select_option(".product_sort_container", "za")
    names = page.locator(".inventory_item_name").all_inner_texts()
    assert names == sorted(names, reverse=True)


def test_responsive_layout_mobile_viewport(page):
    _login(page)
    page.set_viewport_size({"width": 375, "height": 812})
    page.wait_for_selector(".inventory_item")
    assert page.locator(".inventory_item").first.is_visible()


def test_problem_user_visibility_bug_is_detected(page):
    """problem_user is saucedemo's deliberately-broken user - all product
    images render as the same broken image. Used here as a stand-in for a
    'permission tier renders differently' visibility check."""
    _login(page, username="problem_user")
    page.wait_for_selector(".inventory_item")
    images = page.locator(".inventory_item_img img").all()
    srcs = {img.get_attribute("src") for img in images}
    assert len(srcs) == 1