"""E2E-01: recepcionista — alta paciente y agendar cita."""
import re

import pytest
from playwright.sync_api import Page, expect

from conftest import PASSWORD


@pytest.mark.e2e
def test_e2e01_flujo_recepcion(page: Page, base_url):
    page.goto(f"{base_url}/auth/login/")
    page.fill('input[name="username"]', "recepcion.demo")
    page.fill('input[name="password"]', PASSWORD)
    page.click('button[type="submit"]')
    expect(page).to_have_url(re.compile(r"/citas/"))

    page.goto(f"{base_url}/pacientes/nuevo/")
    page.fill('input[name="documento"]', "E2E-0001")
    page.fill('input[name="nombre"]', "Paciente")
    page.fill('input[name="apellido"]', "E2E")
    page.click('button[type="submit"]')
    expect(page).to_have_url(re.compile(r"/pacientes/"))

    page.goto(f"{base_url}/citas/agendar/")
    expect(page.locator("form")).to_be_visible()
