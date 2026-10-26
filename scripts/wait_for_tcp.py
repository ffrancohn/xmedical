#!/usr/bin/env python3
"""Espera a que un puerto TCP acepte conexiones (arranque post-reboot)."""
import socket
import sys
import time

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = int(sys.argv[2] if len(sys.argv) > 2 else "5432")
TIMEOUT_SEC = int(sys.argv[3] if len(sys.argv) > 3 else "90")

deadline = time.monotonic() + TIMEOUT_SEC
while time.monotonic() < deadline:
    try:
        with socket.create_connection((HOST, PORT), timeout=2):
            sys.exit(0)
    except OSError:
        time.sleep(1)

print(f"Timeout: {HOST}:{PORT} no disponible tras {TIMEOUT_SEC}s", file=sys.stderr)
sys.exit(1)
