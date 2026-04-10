from playwright.sync_api import sync_playwright
import time
import os

os.makedirs("screenshots", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    
    BASE_URL = "http://127.0.0.1:8000"
    
    print("Capturing Home...")
    page.goto(f"{BASE_URL}/")
    time.sleep(1)
    page.screenshot(path="screenshots/home.png")
    
    print("Capturing Register...")
    page.goto(f"{BASE_URL}/register")
    time.sleep(1)
    page.screenshot(path="screenshots/register.png")
    
    print("Capturing Login...")
    page.goto(f"{BASE_URL}/login")
    time.sleep(1)
    page.screenshot(path="screenshots/login.png")

    print("Logging in to capture dashboard...")
    page.fill("input[name=username]", "testadmin_final@final.com")
    page.fill("input[name=password]", "securepass123")
    page.click("button[type=submit]")
    time.sleep(2)
    
    print("Capturing Dashboard...")
    page.goto(f"{BASE_URL}/dashboard")
    time.sleep(2)
    page.screenshot(path="screenshots/dashboard.png")
    
    print("Capturing Admin Users List...")
    page.goto(f"{BASE_URL}/admin/users")
    time.sleep(2)
    page.screenshot(path="screenshots/admin_users.png")
    
    print("Capturing Docs UI...")
    page.goto(f"{BASE_URL}/docs")
    time.sleep(2)
    page.screenshot(path="screenshots/docs.png")
    
    browser.close()
    print("Successfully captured all screenshots.")
