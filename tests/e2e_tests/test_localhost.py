from time import sleep
from playwright.sync_api import sync_playwright

LOCAL_TEST_URL = 'http://localhost:8501'

def run_test(input_selector: str, input_value: str, expected_value: str, headless: bool = True) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(LOCAL_TEST_URL)
        page.wait_for_selector(input_selector)
        page.fill(input_selector, input_value)
        page.keyboard.press("Enter")
        sleep(1)
        metric_value = page.locator('div[data-testid="stMetricValue"] div').all_text_contents()[1].strip()
        if metric_value == expected_value.strip():
            print(f"Test Passed! Expected and actual values match: {metric_value}")
        else:
            print(f"Test Failed! Expected '{expected_value}' but got '{metric_value}'.")

        browser.close()

def run_tests() -> None:
    """
    Executes a series of predefined tests by running the 'run_test' function with different input values.
    """
    test_cases = [
        {'input_selector': '#number_input_1', 'input_value': '100000', 'expected_value': '12r 7m'},
        {'input_selector': '#number_input_2', 'input_value': '40000', 'expected_value': '33r 4m'},
        {'input_selector': '#number_input_3', 'input_value': '1000000', 'expected_value': '39r 6m'},
        {'input_selector': '#number_input_1', 'input_value': '-3', 'expected_value': 'Více než 50 let'},
        {'input_selector': '#number_input_2', 'input_value': '-3', 'expected_value': '0r 0m'},
        {'input_selector': '#number_input_3', 'input_value': '-300000', 'expected_value': '47r 1m'}
    ]

    for case in test_cases:
        print(f"\nRunning test for input value: {case['input_value']}")
        run_test(case['input_selector'], case['input_value'], case['expected_value'])

if __name__ == "__main__":
    run_tests()
