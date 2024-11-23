import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture()
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
            slow_mo=3000
        )
        yield browser
        browser.close()

@pytest.fixture()
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

def test_cookies(page):
    print("Navigating to engeto.cz")
    page.goto("https://engeto.cz/")
        

    print("Verifying existing cookies")
    cookies_alert = page.locator("#cookiescript_injected")
    assert cookies_alert.is_visible(), "Cookies alert is not visible"

    print("Verifying header text in cookies")
    assert page.is_visible("#cookiescript_header") , "Text in cookies alert is not visible"

    print("Verifying existing buttons in cookies")
    assert page.is_visible("#cookiescript_reject"), "Reject button is not visible"
    assert page.is_visible("#cookiescript_accept"), "Accept button is not visible"

    print("Cookies accepted")
    cookies_accept = cookies_alert.get_by_role("button", name="Chápu a přijímám!")
    cookies_accept.click()

def test_homepage_content(page):
    print("Navigating to engeto.cz")
    page.goto("https://engeto.cz/")

    print("Verifying existing cookies")
    cookies_alert = page.locator("#cookiescript_injected")

    print("Cookies accepted")
    cookies_accept = cookies_alert.get_by_role("button", name="Chápu a přijímám!")
    cookies_accept.click()

    print("Verifying page title")
    assert page.title() == "Kurzy programování a dalších IT technologií | ENGETO", "Page title is not correct"

    print("Verifying h1")
    assert page.inner_text("h1") == "STAŇ SE NOVÝM IT TALENTEM", "Main header text is incorrect"    

    print("Verifying button")
    assert page.inner_text("body > main > div.block-homepage-header > div > a") == "PŘEHLED IT KURZŮ", "Button text is incorrect" 

    print("Verifying navigation menu")
    assert page.is_visible("#top-navigation"), "Navigation is not visible"

def test_add_to_cart(page):
    print("Navigating to engeto.cz")
    page.goto("https://engeto.cz/")

    print("Verifying existing cookies")
    cookies_alert = page.locator("#cookiescript_injected")

    print("Cookies accepted")
    cookies_accept = cookies_alert.get_by_role("button", name="Chápu a přijímám!")
    cookies_accept.click()
    
    print("Clicking on button Termíny")
    page.click("text=Termíny")

    print("Clicking on checkbox Testování softwaru")
    page.click("#technology-testovani-softwaru")

    print("clicking on first detail course")
    page.click(".block-dates-filter-products > div:nth-child(2) > div:nth-child(2) > .block-button")

    print("clicking on login to this date")
    page.click("text=Přihlas se na termín")

    print("Navigating to cart")
    assert page.url == "https://engeto.cz/cart/", "We are not in cart"

    print("Verifying product in cart")
    assert page.is_visible("body > main > div.woocommerce > form > table > tbody > tr.woocommerce-cart-form__cart-item.cart_item > td.product-remove > a"), "Product is not in cart"