# 🛒 E-Commerce Web Application Automation Using Selenium

## 👨‍🎓 Student Details

| Details | Information |
|---|---|
| **Name** | **Wasim Ahmed** |
| **Stream** | **Computer Science and Technology (CST)** |
| **Section** | **C** |
| **Enrollment Number** | **12023002022233** |
| **Institute Name** | **Institute of Engineering and Management (IEM), Kolkata** |
| **Year** | **4th** |

---

# 📌 Project Name

## **Automate an E-Commerce Web Application Using Selenium WebDriver with Python**

---

## 🎯 Project Description

This project is an automated testing framework developed using **Python, Selenium WebDriver, and Pytest**.

The project automates a customer purchase workflow on an E-Commerce web application. It demonstrates browser automation, login, product search, cart operations, test-data handling, popup/alert handling, screenshots, logging, and execution reporting.

### 🌐 Application

**TutorialsNinja Demo Store**

https://tutorialsninja.com/demo/

---

## 🔄 Automated Test Flow

```text
Launch Browser
      ↓
Open E-Commerce Website
      ↓
Register / Login
      ↓
Search Product
      ↓
Select Product
      ↓
Add Product to Cart
      ↓
Update Quantity
      ↓
Verify Cart Details
      ↓
Handle Popups / Alerts
      ↓
Capture Screenshots
      ↓
Generate Execution Report
```

---

## 🛠️ Technologies Used

- **Python**
- **Selenium WebDriver**
- **Pytest**
- **Pytest-HTML**
- **Excel**
- **JSON**
- **Page Object Model (POM)**
- **Git**
- **GitHub**
- **GitHub Actions**

---

## 📂 Project Structure

```text
ecommerce-selenium-framework/
│
├── pages/
│   ├── base_page.py
│   ├── register_page.py
│   ├── login_page.py
│   ├── home_page.py
│   ├── search_results_page.py
│   └── cart_page.py
│
├── tests/
│   └── test_purchase_flow.py
│
├── testdata/
│   ├── products.xlsx
│   └── test_data.json
│
├── config/
│   └── config.json
│
├── utils/
│   ├── data_reader.py
│   ├── driver_factory.py
│   ├── logger.py
│   └── screenshot.py
│
├── reports/
│   └── screenshots/
│
├── logs/
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## ✅ Features Automated

### 1. Browser Launch
Launches the selected browser using Selenium WebDriver.

### 2. Registration and Login
Automates user registration and login functionality.

### 3. Product Search
Searches for products available on the E-Commerce website.

### 4. Add to Cart
Selects the required product and adds it to the shopping cart.

### 5. Update Quantity
Updates the quantity of the selected product in the cart.

### 6. Cart Verification
Verifies product name, quantity, unit price, total price, and cart details.

### 7. Popup and Alert Handling
Handles JavaScript alerts and HTML success/error notification banners.

### 8. Screenshot Capture
Captures screenshots during important test steps and failures.

### 9. Data-Driven Testing
Reads product and test information from Excel and JSON files.

### 10. Execution Reporting
Generates an HTML test execution report using Pytest-HTML.

---

## 🚨 Popup and Alert Handling

The framework contains reusable popup-handling functionality in:

```text
pages/base_page.py
```

JavaScript alerts are handled using Selenium's:

```python
driver.switch_to.alert
```

The framework also handles HTML notification banners such as:

```text
Success: You have added a product to your shopping cart!
```

This makes the automation more reliable when notifications or alerts appear during execution.

---

## 📊 Test Data

### Excel

Product test data is maintained in:

```text
testdata/products.xlsx
```

### JSON

Registration and login-related test data is maintained in:

```text
testdata/test_data.json
```

---

## ▶️ How to Run the Project

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ecommerce-selenium-automation.git
cd ecommerce-selenium-automation
```

### Step 2: Create virtual environment

```bash
python -m venv .venv
```

### Step 3: Activate virtual environment

Windows:

```bash
.venv\Scripts\activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run all tests

```bash
pytest
```

### Run a specific test

```bash
pytest -k TC01_MacBook
```

### Run in headless mode

```bash
pytest --headless
```

---

## 📄 Test Execution Report

After execution, the HTML report is generated in:

```text
reports/execution_report.html
```

Screenshots are stored in:

```text
reports/screenshots/
```

Logs are stored in:

```text
logs/
```

---

## 🧪 Testing Framework

This project follows the **Page Object Model (POM)** design pattern.

Benefits:

- Better code organization
- Reusable page methods
- Easier maintenance
- Reduced code duplication
- Separation of test logic and page interaction

---

## 🎓 Learning Outcomes

Through this project, I gained practical knowledge of:

- Selenium WebDriver
- Python automation testing
- Pytest
- Page Object Model
- Explicit waits
- XPath and CSS selectors
- Popup and alert handling
- Data-driven testing
- Excel and JSON test data
- Screenshot capture
- HTML reporting
- Logging
- Git and GitHub
- CI/CD using GitHub Actions

---

## 👨‍💻 Student / Developer

**Wasim Ahmed**

**Stream:** Computer Science and Technology (CST)

**Section:** C

**Enrollment Number:** 12023002022233

**University:** Institute of Engineering and Management (IEM), Kolkata

---

## 🔗 Project Repository

**GitHub:**  
https://github.com/wasim9658/Selenium_Capstone_Project/tree/main/ecommerce-selenium-framework

---

## ⭐ Project Summary

This project demonstrates an end-to-end automated E-Commerce testing framework using Selenium WebDriver with Python. It follows the Page Object Model, supports data-driven testing, handles popups and alerts, captures screenshots, generates execution reports, and can be integrated with GitHub Actions for continuous testing.

---

### © 2026 Wasim Ahmed
