"""Escenarios de carga Locust (LOAD-*)."""
import os

from locust import HttpUser, between, task

BASE = os.environ.get("XMEDICAL_BASE_URL", "https://xmedical.cloud")


class AnonymousUser(HttpUser):
    wait_time = between(1, 3)
    host = BASE

    @task
    def load_01_login_page(self):
        self.client.get("/auth/login/", name="LOAD-01 login")


class MedicoUser(HttpUser):
    wait_time = between(1, 3)
    host = BASE
    weight = 2

    def on_start(self):
        self.client.post(
            "/auth/login/",
            {"username": "medico.demo", "password": "Xmedical123!"},
            name="login medico",
        )

    @task
    def load_02_dashboard(self):
        self.client.get("/dashboard/", name="LOAD-02 dashboard")


class RecepcionUser(HttpUser):
    wait_time = between(1, 3)
    host = BASE
    weight = 2

    def on_start(self):
        self.client.post(
            "/auth/login/",
            {"username": "recepcion.demo", "password": "Xmedical123!"},
            name="login recepcion",
        )

    @task
    def load_03_pacientes(self):
        self.client.get("/pacientes/", name="LOAD-03 pacientes")
