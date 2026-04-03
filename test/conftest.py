import sys
import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

sys.path.insert(0, str(Path(__file__).parent))

SCREENSHOTS_DIR = Path(__file__).parent / "reports" / "screenshots"


@pytest.fixture(scope="session")
def driver():
    opts = Options()
    opts.add_argument("--ignore-certificate-errors")
    opts.add_argument("--allow-file-access-from-files")
    opts.add_argument("--disable-web-security")
    # print(opts.arguments)
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=opts)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    print(item.name)
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if call.when == "call" and "driver" in item.funcargs:
        # print(call.excinfo)
        driver = item.funcargs["driver"]
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

        safe_name = "".join(c if c.isalnum() or c in "_-" else "_" for c in item.name)
        path = SCREENSHOTS_DIR / f"{safe_name}.png"
        driver.save_screenshot(str(path))

        if pytest_html:
            extra.append(pytest_html.extras.image(str(path)))

    report.extra = extra
