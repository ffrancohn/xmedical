# syntax=docker/dockerfile:1
# CPython 3.11.18+ (parche compilado; build_cpython_patch.sh)
FROM python:3.11.17-slim-bookworm AS infosec_python311
COPY build_cpython_patch.sh /tmp/build_cpython_patch.sh
RUN PYTHON_VERSION=3.11.18 sh /tmp/build_cpython_patch.sh && rm /tmp/build_cpython_patch.sh
RUN python -m pip install --no-cache-dir --upgrade pip

FROM infosec_python311

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . /app/

ENV PATH="/app/.venv/bin:$PATH"

CMD ["gunicorn", "xmedical.wsgi:application", "--bind", "0.0.0.0:8000"]
