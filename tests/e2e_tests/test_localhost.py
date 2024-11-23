from time import sleep
from playwright.sync_api import sync_playwright

LOCAL_TEST_URL = 'http://localhost:8501'

def run_test(input_selector, input_value, expected_value, headless=False):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(LOCAL_TEST_URL)  
        page.wait_for_selector(input_selector)
        page.fill(input_selector, input_value)
        page.keyboard.press("Enter")
        sleep(2)
        metric_value = page.locator('div[data-testid="stMetricValue"] div').all_text_contents()[1]
        if metric_value.strip() == expected_value.strip():
            print(f"Value is correct! ({metric_value.strip()})")
        else:
            print(f"Expected value '{expected_value.strip()}' does not match the actual value '{metric_value.strip()}'.")
        browser.close()

def run():
    test_cases = [
        {
            'input_selector': '#number_input_1',
            'input_value': '100000',
            'expected_value': '12r 7m'
        },
        {
            'input_selector': '#number_input_2',
            'input_value': '40000',
            'expected_value': '33r 4m'
        },
        {
            'input_selector': '#number_input_3',
            'input_value': '1000000',
            'expected_value': '39r 6m'
        },
        {
            'input_selector': '#number_input_1',
            'input_value': '-3',
            'expected_value': 'Více než 50 let'
        },
        {
            'input_selector': '#number_input_2',
            'input_value': '-3',
            'expected_value': '0r 0m'
        },
        {
            'input_selector': '#number_input_3',
            'input_value': '-300000',
            'expected_value': '47r 1m'
        },
    ]

    for case in test_cases:
        print(f"Running test for value: {case['input_value']}")
        run_test(case['input_selector'], case['input_value'], case['expected_value'])

run()
