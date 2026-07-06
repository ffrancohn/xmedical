"""Utilidades compartidas para tests de XMedical."""
from django.test import Client

PASSWORD = "Xmedical123!"
HOST = {"HTTP_HOST": "xmedical.cloud"}
FIXTURES = ["initial_data.json"]


def auth_client(username):
    client = Client(**HOST)
    assert client.login(username=username, password=PASSWORD), f"Login fallo: {username}"
    return client
