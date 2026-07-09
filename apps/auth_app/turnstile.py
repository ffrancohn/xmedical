import json
import logging
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.conf import settings

logger = logging.getLogger(__name__)

TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


def is_turnstile_enabled():
    return bool(
        getattr(settings, "TURNSTILE_ENABLED", False)
        and getattr(settings, "TURNSTILE_SITE_KEY", "")
        and getattr(settings, "TURNSTILE_SECRET_KEY", "")
    )


def get_client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def verify_turnstile(token, remote_ip=None):
    if not token:
        return False

    secret = settings.TURNSTILE_SECRET_KEY
    if not secret:
        return False

    payload = {"secret": secret, "response": token}
    if remote_ip:
        payload["remoteip"] = remote_ip

    try:
        req = Request(
            TURNSTILE_VERIFY_URL,
            data=urlencode(payload).encode(),
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        with urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        return data.get("success", False)
    except (URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        logger.warning("Turnstile verification failed: %s", exc)
        return False
