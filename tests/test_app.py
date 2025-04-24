import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "base_url": "http://localhost:5001"}

def test_homepage_loads(page: Page):
    page.goto("/")
    expect(page).to_have_title("Kviz Znanja")
    expect(page.get_by_text("Dobro došli u Kviz Znanja!")).to_be_visible()
    expect(page.get_by_role("link", name="Započni Kviz")).to_be_visible()

def test_quiz_flow(page: Page):
    page.goto("/")
    page.click("a >> text=Započni Kviz")
    expect(page).to_have_title("Kviz - Pitanje 1")
    expect(page.get_by_text("Pitanje 1 od 3")).to_be_visible()
    
    # Odgovori na prvo pitanje
    page.wait_for_selector("input[type='radio']", state="visible", timeout=10000)
    page.locator("input[type='radio']").first.check()
    page.click("button >> text=Pošalji")
    expect(page).to_have_title("Kviz - Pitanje 2")
    
    # Odgovori na drugo pitanje
    page.wait_for_selector("input[type='radio']", state="visible", timeout=10000)
    page.locator("input[type='radio']").first.check()
    page.click("button >> text=Pošalji")
    expect(page).to_have_title("Kviz - Pitanje 3")
    
    # Odgovori na treće pitanje
    page.wait_for_selector("input[type='radio']", state="visible", timeout=10000)
    page.locator("input[type='radio']").first.check()
    page.click("button >> text=Pošalji")
    
    # Provjeri rezultat
    expect(page.get_by_text("Vaš rezultat:")).to_be_visible()
    expect(page.get_by_text("Igraj ponovo")).to_be_visible()
