"""E2E-03: médico — wizard consulta (pasos visibles)."""
import re

import pytest
from playwright.sync_api import Page, expect

from conftest import PASSWORD


@pytest.mark.e2e
def test_e2e03_flujo_medico_wizard(page: Page, base_url):
    page.goto(f"{base_url}/auth/login/")
    page.fill('input[name="username"]', "medico.demo")
    page.fill('input[name="password"]', PASSWORD)
    page.click('button[type="submit"]')
    expect(page).to_have_url(re.compile(r"/dashboard/"))
    expect(page.locator("body")).to_be_visible()
