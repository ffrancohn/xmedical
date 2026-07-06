"""E2E-05: logout — sesión cerrada."""
import re

import pytest
from playwright.sync_api import Page, expect

from conftest import PASSWORD


@pytest.mark.e2e
def test_e2e05_logout(page: Page, base_url):
    page.goto(f"{base_url}/auth/login/")
    page.fill('input[name="username"]', "medico.demo")
    page.fill('input[name="password"]', PASSWORD)
    page.click('button[type="submit"]')
    expect(page).to_have_url(re.compile(r"/dashboard/"))

    page.goto(f"{base_url}/auth/logout/")
    page.goto(f"{base_url}/dashboard/")
    expect(page).to_have_url(re.compile(r"/auth/login/"))
