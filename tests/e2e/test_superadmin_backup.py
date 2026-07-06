"""E2E-04: superadmin — panel global."""
import re

import pytest
from playwright.sync_api import Page, expect

from conftest import PASSWORD


@pytest.mark.e2e
def test_e2e04_superadmin_panel(page: Page, base_url):
    page.goto(f"{base_url}/auth/login/")
    page.fill('input[name="username"]', "superadmin.demo")
    page.fill('input[name="password"]', PASSWORD)
    page.click('button[type="submit"]')
    expect(page).to_have_url(re.compile(r"/superadmin/"))
    expect(page.locator("body")).to_contain_text("Superadmin")
