# E-Commerce Purchase Flow – Selenium WebDriver + Python (Capstone)

End-to-end UI automation of a customer buying a product on the public
**[TutorialsNinja demo store](https://tutorialsninja.com/demo/)** (OpenCart).
Built with **Selenium 4, Python, pytest, Page Object Model**, data-driven from **Excel + JSON**,
with **screenshots** and a self-contained **HTML execution report**.

## Business scenario → automation mapping

| # | Requirement | Where it is implemented |
|---|-------------|-------------------------|
| 1 | Launch browser | `driver` fixture in `conftest.py`, `utils/driver_factory.py` (Chrome / Firefox / Edge, headless option) |
| 2 | Login | `pages/login_page.py`; a fresh account is created per test by the `registered_user` fixture |
| 3 | Search product | `HomePage.search()` → `SearchResultsPage` |
| 4 | Add to cart | `SearchResultsPage.add_to_cart()` |
| 5 | Update quantity | `CartPage.update_quantity()` |
| 6 | Verify cart details | assertions on presence, quantity, unit price × qty = line total, header cart count, grand total |
| 7 | Screenshots | `snap` fixture → `reports/screenshots/` (auto-capture on failure too) |
| 8 | Data from Excel / JSON | `testdata/products.xlsx` (products, quantities, Run flag) and `testdata/test_data.json` (user profile, negative-login data) |
| 9 | Popups / alerts | `BasePage.handle_alert_if_present()` (native JS alerts) and `close_banners()` (HTML alert banners) |
| 10 | Execution report | `reports/execution_report.html` (pytest-html, screenshots embedded) |

## Project structure

```
ecommerce-selenium-framework/
├── config/config.json          # base URL, browser, headless, timeouts
├── testdata/
│   ├── products.xlsx           # data-driven scenarios (one row = one test)
│   └── test_data.json          # user profile + negative login data
├── pages/                      # Page Object Model
│   ├── base_page.py            # waits, safe click, alert/popup handling
│   ├── register_page.py  login_page.py  home_page.py
│   ├── search_results_page.py  cart_page.py
├── utils/                      # driver factory, Excel/JSON reader, screenshot, logger
├── tests/test_purchase_flow.py # test scenarios
├── conftest.py                 # fixtures + report hooks
├── pytest.ini  requirements.txt
├── reports/                    # HTML report + screenshots (generated)
└── logs/execution.log          # run log (generated)
```

## Setup

Requires Python 3.10+ and Google Chrome (Firefox / Edge also supported).
Selenium 4.6+ downloads the matching driver automatically – no manual driver setup.

```bash
git clone <your-repo-url>
cd ecommerce-selenium-framework
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
pytest                              # full run, headed Chrome (good for demos)
pytest --headless                   # no browser window (CI)
pytest --browser firefox            # other browsers: chrome | firefox | edge
pytest -k TC01_MacBook              # a single Excel scenario
pytest -m smoke                     # only tests marked smoke
```

Open **`reports/execution_report.html`** in a browser afterwards – it lists every test with
its status, duration, log output and the embedded screenshots from each step.

## Test data

* **Excel** – `testdata/products.xlsx`, sheet `Products`

  | TestCase ID | Run | Search Term | Product Name | Update Quantity |
  |---|---|---|---|---|
  | TC01_MacBook | Y | MacBook | MacBook | 3 |

  Add a row to add a test. Set `Run` to `N` to skip it. (`python -m utils.create_test_excel` regenerates the sample file.)
* **JSON** – `testdata/test_data.json` holds the registration profile and the negative-login expectations.
* **Config** – `config/config.json` (change `base_url` to point at another OpenCart-based demo).

## Design notes

* **Page Object Model** – locators and page behaviour live in `pages/`; tests read like the business flow.
* **Explicit waits only** – no `time.sleep`; `WebDriverWait` + expected conditions everywhere.
* **Test isolation** – each test registers its own unique user, so cart contents never leak between tests
  or depend on other people using the public demo.
* **Robust clicking** – scroll into view, JS-click fallback when an element is intercepted.
* **Failure evidence** – a screenshot is captured automatically when a test fails and embedded in the report.

## Troubleshooting

* *Timeouts / site slow* – the public demo can be slow; raise `explicit_wait` in `config/config.json`.
* *Product not found in results* – the demo store data can be edited by others; check the exact name in `products.xlsx`.
* *Products with required options* (e.g. Apple Cinema 30") cannot be added from the listing page – use simple products.

## Author

Your Name · [LinkedIn](https://linkedin.com/in/your-profile) · [GitHub](https://github.com/your-username)
