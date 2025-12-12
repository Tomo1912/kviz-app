import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "base_url": "http://localhost:5001"}

def test_homepage_loads(page: Page):
    page.goto("/")
    expect(page).to_have_title("DevOps Knowledge Test")
    expect(page.get_by_text("Welcome to DevOps Knowledge Test!")).to_be_visible()
    expect(page.get_by_role("link", name="Start Quiz")).to_be_visible()

def test_quiz_flow(page: Page):
    page.goto("/")
    page.click("a >> text=Start Quiz")
    expect(page).to_have_title("Quiz - Question 1")
    expect(page.get_by_text("Question 1 of 10")).to_be_visible()
    
    # Answer first question
    page.wait_for_selector("input[type='radio']", state="visible", timeout=10000)
    page.locator("input[type='radio']").first.check()
    page.click("button >> text=Submit")
    expect(page).to_have_title("Quiz - Question 2")
    
    # Answer remaining questions (2-10)
    for i in range(2, 11):
        page.wait_for_selector("input[type='radio']", state="visible", timeout=10000)
        page.locator("input[type='radio']").first.check()
        page.click("button >> text=Submit")
        if i < 10:
            expect(page).to_have_title(f"Quiz - Question {i + 1}")
    
    # Check results
    expect(page.get_by_text("Your Score:")).to_be_visible()
    expect(page.get_by_text("Play Again")).to_be_visible()
