"""Create WebDriver instances. Selenium 4.6+ downloads the right driver automatically
(Selenium Manager), so no webdriver-manager package is needed."""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def create_driver(browser: str = "chrome", headless: bool = False,
                  window_size: str = "1366,900", page_load_timeout: int = 60):
    browser = browser.lower()
    width, height = window_size.split(",")

    if browser == "chrome":
        opts = ChromeOptions()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument(f"--window-size={width},{height}")
        opts.add_argument("--disable-notifications")   # suppress browser popups
        opts.add_argument("--disable-infobars")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Chrome(options=opts)
    elif browser == "firefox":
        opts = FirefoxOptions()
        if headless:
            opts.add_argument("-headless")
        opts.add_argument(f"--width={width}")
        opts.add_argument(f"--height={height}")
        driver = webdriver.Firefox(options=opts)
    elif browser == "edge":
        opts = EdgeOptions()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument(f"--window-size={width},{height}")
        driver = webdriver.Edge(options=opts)
    else:
        raise ValueError(f"Unsupported browser: {browser!r} (use chrome, firefox or edge)")

    driver.set_page_load_timeout(page_load_timeout)
    if not headless:
        driver.maximize_window()
    return driver
