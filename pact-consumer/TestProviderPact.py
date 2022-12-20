import logging
import pytest

from pact import Verifier

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


PACT_BROKER_URL = "http://192.168.1.187:9292"
PROVIDER_HOST = "localhost"
PROVIDER_PORT = 8000
PROVIDER_URL = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"


@pytest.fixture
def broker_opts():
    return {
        "broker_url": PACT_BROKER_URL,
        "publish_version": "3",
        "publish_verification_results": True,
    }


def test_weathersrvc(broker_opts):
    verifier = Verifier(provider="WeatherService", provider_base_url=PROVIDER_URL)

    success, logs = verifier.verify_with_broker(
        **broker_opts,
        verbose=True,
        enable_pending=False,
    )

    if (success != 0):
       print(logs)

    assert success == 0
