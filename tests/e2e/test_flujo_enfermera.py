"""E2E-02: enfermera — preclínica."""
import re

import pytest
from playwright.sync_api import Page, expect

from conftest import PASSWORD


@pytest.mark.e2e
def test_e2e02_flujo_enfermera(page: Page, base_url):
    page.goto(f"{base_url}/auth/login/")
    page.fill('input[name="username"]', "enfermera.demo")
    page.fill('input[name="password"]', PASSWORD)
    page.click('button[type="submit"]')
    expect(page).to_have_url(re.compile(r"/preclinica/"))
    expect(page.locator("body")).to_contain_text("Preclinica")
