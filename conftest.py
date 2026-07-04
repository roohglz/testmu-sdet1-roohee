"""
conftest.py - pytest hooks and shared fixtures

Wires the LLM Failure Explainer into every test run, and provides a
Playwright `page` fixture used by the Login and Dashboard tests.
"""

import pytest
from playwright.sync_api import sync_playwright
from src.failure_explainer import explain_failure, save_explanation


@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        pg = context.new_page()
        yield pg
        context.close()
        browser.close()


@pytest.fixture(autouse=True)
def _init_failure_context(request):
    request.node.failure_context = {}
    yield


def attach_context(request, **kwargs):
    """Call from inside a test to attach extra context before it might fail,
    e.g. attach_context(request, status_code=resp.status_code)"""
    request.node.failure_context.update(kwargs)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        test_name = item.nodeid
        error_message = str(call.excinfo.value) if call.excinfo else "Unknown error"
        context = getattr(item, "failure_context", {})

        if "page" in item.funcargs:
            pg = item.funcargs["page"]
            try:
                context["page_url"] = pg.url
                context["page_title"] = pg.title()
            except Exception:
                pass

        try:
            explanation = explain_failure(test_name, error_message, context)
            save_explanation(test_name, explanation)

            print(f"\n{'='*60}")
            print(f"LLM FAILURE ANALYSIS: {test_name}")
            print(f"{'='*60}")
            print(f"Summary:    {explanation.get('summary')}")
            print(f"Cause:      {explanation.get('likely_cause')}")
            print(f"Fix:        {explanation.get('suggested_fix')}")
            print(f"Confidence: {explanation.get('confidence')}")
            print(f"{'='*60}\n")
        except Exception as e:
            print(f"\n[Failure Explainer error - skipping analysis]: {e}\n")