import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture()
def browser():
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(
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

def test_page_load(page):
    print("Navigating to cvoxdesign.com")
    response = page.goto("https://cvoxdesign.com/")

    print("Verifying page load")
    assert response.status == 200, "Page did not load successfully"

    print("Verifying page title")
    assert page.title() == "cv0x Design", "Page title is not correct"

    print("Verifying logo")
    assert page.is_visible("#home > div.home-img > img"), "Logo is not visible"

    print("Verifying navigation")
    assert page.is_visible("nav"), "Navigation is not visible"

    print("Verifying header")
    assert page.is_visible("#home > div.home-content > h1"), "header 1 is not visible"
    assert page.is_visible("#home > div.home-content > h3"), "header 3 is not visible"

    print("Verifying social bar")
    assert page.is_visible("#home > div.home-content > div.social"), "social bar is not visible"


def test_navigation_menu(page):  
    print("Navigating to cvoxdesign.com")
    page.goto("https://cvoxdesign.com/")  

    print("Verifying navigation items")
    nav_text = page.locator("nav").text_content()
    expected_items = ["Domů", "O mně", "Služby", "Tvorba", "Kontakt"]
    for item in expected_items:
        assert item in nav_text, f"'{item}' not found in navigation menu."

    print("Navigating to Domů")
    page.click("text=Domů")
    assert page.url == "https://cvoxdesign.com/#home", "Navigation to Domů failed"

    print("Navigating to O mně")
    page.click("text=O mně")
    assert page.url == "https://cvoxdesign.com/#about", "Navigation to O mně failed"

    print("Navigating to Služby")
    page.click("text=Služby")
    assert page.url == "https://cvoxdesign.com/#services", "Navigation to Služby failed"

    print("Navigating to Tvorba")
    page.click("text=Tvorba")
    assert page.url == "https://cvoxdesign.com/#portfolio", "Navigation to Tvorba failed"

    print("Navigating to Kontakt")
    page.click("text=Kontakt")
    assert page.url == "https://cvoxdesign.com/#contact", "Navigation to Kontakt failed"


def test_form_submission(page):
    print("Navigating to cvoxdesign.com Kontakt")
    page.goto("https://cvoxdesign.com/#contact")

    print("Filling form")
    page.fill("input[id='name']", "Test User")
    page.fill("input[id='email']", "test@tester.cz")
    page.fill("textarea[id='message']", "This is a test message :)")

    page.on("dialog", lambda dialog: print(dialog.message))
    print("Submitting form")
    page.click("text=Odeslat zprávu")
    print("Accepting dialog")


def test_empty_form_submission(page):
    print("Navigating to cvoxdesign.com Kontakt")
    page.goto("https://cvoxdesign.com/#contact")

    print("sending an empty form")
    page.click("text=Odeslat zprávu")
    assert page.is_visible("text=Please fill out this field"), "Validation error not shown"
