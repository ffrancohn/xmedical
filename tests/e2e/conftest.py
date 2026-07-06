"""Configuración base para pruebas E2E con Playwright."""
import os

import pytest

BASE_URL = os.environ.get("XMEDICAL_BASE_URL", "https://xmedical.cloud")
PASSWORD = os.environ.get("XMEDICAL_TEST_PASSWORD", "Xmedical123!")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "ignore_https_errors": True}


@pytest.fixture
def base_url():
    return BASE_URL
