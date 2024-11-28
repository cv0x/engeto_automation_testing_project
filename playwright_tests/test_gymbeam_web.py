import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture()
def browser():
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(
            headless=False,
            slow_mo=1000
        )
        yield browser
        browser.close()

@pytest.fixture()
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

def test_product_search_by_name(page):
    print("Navigating to gymbeam.cz")
    page.goto("https://www.gymbeam.cz/")

    print("Waiting for cookies to load")
    page.wait_for_timeout(300)

    print("Refusing cookies")
    page.get_by_role("button", name="Odmítnout").click()

    print("Searching for 'Vitamín D3'")
    page.fill("input[data-test=\"common-autocomplete-input\"]", "Vitamín D3")
    page.press("input[data-test=\"common-autocomplete-input\"]", "Enter")

    print("Waiting for products to load")
    page.wait_for_timeout(1000)

    print("Verifying search results")
    assert page.is_visible("text=Vitamín D3"), "Search results do not include 'Vitamín D3'"

    print("test_product_search_by_name passed ✅") 


def test_product_search_by_category(page):
    print("Navigating to gymbeam.cz")
    page.goto("https://www.gymbeam.cz/")
    
    print("Waiting for cookies to load")
    page.wait_for_timeout(300)

    print("Refusing cookies")
    page.get_by_role("button", name="Odmítnout").click()

    print("Searching for category 'Proteiny'")
    page.fill("input[data-test=\"common-autocomplete-input\"]", "Proteiny")
    page.press("input[data-test=\"common-autocomplete-input\"]", "Enter")

    print("Waiting for products to load")
    page.wait_for_timeout(1000)  

    print("Verifying search results")
    assert page.is_visible("text=Protein"), "Search results do not match category 'Proteiny'"

    print("test_product_search_by_category passed ✅") 


def test_price_filter(page):
    print("Navigating to gymbeam.cz/proteiny with price filter 500-650")
    page.goto("https://gymbeam.cz/proteiny?filter=out&price=500.00-650.00")

    print("Waiting for cookies to load")
    page.wait_for_timeout(300)

    print("Refusing cookies")
    page.get_by_role("button", name="Odmítnout").click()

    print("Waiting for products to load")
    page.wait_for_timeout(500) 

    print("Verifying product prices")   
    prices = page.query_selector_all("span.normal-price")
    for price in prices:
        value = int(price.inner_text().replace("Kč", "").strip())
        assert 500 <= value <= 650, f"Product price {value} is out of range"

    print("test_price_filter passed ✅") 


def test_add_product_to_cart(page):
    print("Navigating to gymbeam.cz/protein-true-whey-gymbeam")
    page.goto("https://gymbeam.cz/protein-true-whey-gymbeam.html")

    print("Waiting for cookies to load")
    page.wait_for_timeout(300)

    print("Refusing cookies")
    page.get_by_role("button", name="Odmítnout").click()

    print("Adding product to cart")
    page.click("button[data-test=\"pdp-add-to-cart-main\"]")

    print("Waiting for product to be added to cart")
    page.wait_for_timeout(1000)

    print("Navigating to cart")
    page.goto("https://gymbeam.cz/checkout/cart/")
        
    print("Verifying product in cart")
    assert page.is_visible("text=True Whey - GymBeam"), "Product not found in cart"

    print("test_add_product_to_cart passed ✅")