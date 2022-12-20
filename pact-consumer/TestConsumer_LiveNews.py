import atexit
import logging
import os
import pytest

from src.consumer import WeatherConsumer,Weather
from pact import Consumer,Provider,EachLike,Like


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


PACT_BROKER_URL = "http://192.168.1.187:9292"


# Define where to run the mock server, for the consumer to connect to. These
# are the defaults so may be omitted
PACT_MOCK_HOST = "localhost"
PACT_MOCK_PORT = 1234

# Where to output the JSON Pact files created by any tests
PACT_DIR = "./pacts"


@pytest.fixture
def consumer() -> WeatherConsumer:
    return WeatherConsumer("http://{host}:{port}".format(host=PACT_MOCK_HOST, port=PACT_MOCK_PORT))


@pytest.fixture(scope="session")
def pact(request):

    version = "1.0.0"
    publish = True if version else False

    pact = Consumer("LiveNewsService", version=version).has_pact_with(
        Provider("WeatherService"),
        host_name=PACT_MOCK_HOST,
        port=PACT_MOCK_PORT,
        pact_dir=PACT_DIR,
        publish_to_broker=publish,
        broker_base_url=PACT_BROKER_URL
         )

    pact.start_service()

    # Make sure the Pact mocked provider is stopped when we finish, otherwise
    # port 1234 may become blocked
    atexit.register(pact.stop_service)

    yield pact

    # This will stop the Pact mock server, and if publish is True, submit Pacts
    # to the Pact Broker
    pact.stop_service()

    pact.publish_to_broker = True


def test_getWeatherForecast(pact, consumer):
    # Define the Matcher; the expected structure and content of the response
    expected = {
    "date": "2022-12-15",
    "temperatureC": 30,
    "temperatureF": 85,
    "summary": "Hot"
    }

    (
        pact.given("NewsHour service exists")
        .upon_receiving("a request to get weather list for news")
        .with_request("get", "/forecast")
        .will_respond_with(200, body=EachLike(expected))
    )

    with pact:
        # Perform the actual request
    
        user = consumer.get_livenews()
       
        # In this case the mock Provider will have returned a valid response
        assert user[0]['summary'] == "Hot"

        # Make sure that all interactions defined occurred
        pact.verify()


