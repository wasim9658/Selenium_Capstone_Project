"""Shared fixtures and pytest-html report customisation."""
import base64
import os
import time
import uuid
from pathlib import Path

import pytest
from pytest_html import extras as html_extras

from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from utils.data_reader import get_config, get_json_test_data
from utils.driver_factory import create_driver
from utils.logger import get_logger
from utils.screenshot import take_screenshot

log = get_logger("conftest")


# --------------------------------------------------------------------- options
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=None,
                     help="chrome | firefox | edge (overrides config.json)")
    parser.addoption("--headless", action="store_true", default=False,
                     help="run the browser without a UI (overrides config.json)")


def pytest_configure(config):
    Path("reports/screenshots").mkdir(parents=True, exist_ok=True)
    try:  # add rows to the "Environment" table at the top of the HTML report
        from pytest_metadata.plugin import metadata_key
        cfg = get_config()
        meta = config.stash[metadata_key]
        meta["Application Under Test"] = cfg["base_url"]
        meta["Browser"] = config.getoption("--browser") or cfg["browser"]
        meta["Headless"] = str(config.getoption("--headless") or cfg["headless"])
        meta["Project"] = "E-Commerce Selenium Capstone"
    except Exception:  # metadata is cosmetic only
        pass


def pytest_html_report_title(report):
    report.title = "E-Commerce Purchase Flow - Selenium Execution Report"


# ------------------------------------------------------------------- fixtures
@pytest.fixture(scope="session")
def config() -> dict:
    return get_config()


@pytest.fixture(scope="session")
def test_data() -> dict:
    return get_json_test_data()


@pytest.fixture
def driver(request, config):
    """Step 1 - launch the browser (a fresh one per test for isolation)."""
    browser = request.config.getoption("--browser") or config["browser"]
    headless = request.config.getoption("--headless") or config["headless"]
    log.info("Launching %s (headless=%s)", browser, headless)
    drv = create_driver(browser, headless, config["window_size"], config["page_load_timeout"])
    yield drv
    drv.quit()
    log.info("Browser closed")


@pytest.fixture
def snap(request, driver):
    """Call snap('step name') to save a screenshot and attach it to the HTML report."""
    request.node._screenshots = []

    def _snap(step: str) -> Path:
        path = take_screenshot(driver, request.node.name, step)
        request.node._screenshots.append((step, path))
        log.info("Screenshot saved: %s", path.name)
        return path

    return _snap


@pytest.fixture
def registered_user(driver, config, test_data):
    """Precondition: create a brand-new account so the test never depends on shared
    data (the demo store is public and is reset by other users), then log out so the
    test itself can exercise the Login step."""
    u = test_data["user"]
    email = f"{u['email_prefix']}.{int(time.time())}.{uuid.uuid4().hex[:6]}@{u['email_domain']}"
    log.info("Registering precondition user %s", email)

    RegisterPage(driver, config["base_url"], config["explicit_wait"]).load().register(
        u["first_name"], u["last_name"], email, u["telephone"], u["password"])
    LoginPage(driver, config["base_url"], config["explicit_wait"]).logout()
    return {"email": email, "password": u["password"]}


# ---------------------------------------------------------------- report hooks
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshots to the HTML report; grab an extra one when a test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    shots = getattr(item, "_screenshots", [])
    driver = item.funcargs.get("driver")
    if report.failed and driver is not None:
        try:
            path = take_screenshot(driver, item.name, "FAILURE")
            shots.append(("FAILURE", path))
        except Exception as exc:  # browser may already be dead
            log.error("Could not capture failure screenshot: %s", exc)

    report_extras = getattr(report, "extras", [])
    for step, path in shots:
        if os.path.exists(path):
            encoded = base64.b64encode(Path(path).read_bytes()).decode("utf-8")
            report_extras.append(html_extras.png(encoded, name=step))
    report.extras = report_extras
