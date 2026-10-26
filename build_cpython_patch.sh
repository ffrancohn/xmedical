#!/bin/sh
# Instala un parche de CPython sobre la imagen oficial hasta que exista python:X.Y.Z-slim en Hub.
# CVE-2026-115557, CVE-2026-114583 (3.11.18+).
set -eu

PYTHON_VERSION="${PYTHON_VERSION:?PYTHON_VERSION requerido, ej. 3.11.18}"

apt-get update
apt-get install -y --no-install-recommends \
    ca-certificates wget \
    build-essential libssl-dev zlib1g-dev libncursesw5-dev libreadline-dev \
    libsqlite3-dev libffi-dev libbz2-dev liblzma-dev

wget -q "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz" -O /tmp/python.tgz
mkdir -p /usr/src/python
tar -xzf /tmp/python.tgz -C /usr/src/python --strip-components=1
cd /usr/src/python
./configure --prefix=/usr/local --with-ensurepip=install
make -j"$(nproc)"
make install
python3 --version | grep -F "${PYTHON_VERSION}"

apt-get purge -y --auto-remove \
    wget build-essential libssl-dev zlib1g-dev libncursesw5-dev libreadline-dev \
    libsqlite3-dev libffi-dev libbz2-dev liblzma-dev
apt-get autoremove -y
rm -rf /var/lib/apt/lists/* /usr/src/python /tmp/python.tgz
