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

    pact = Consumer("ProductService", version=version).has_pact_with(
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
        pact.given("Weather list exists in the database")
        .upon_receiving("a request to get weather list")
        .with_request("get", "/forecast")
        .will_respond_with(200, body=EachLike(expected))
    )

    with pact:
        # Perform the actual request
    
        user = consumer.get_weather()
       
        # In this case the mock Provider will have returned a valid response
        assert user[0]['summary'] == "Hot"

        # Make sure that all interactions defined occurred
        pact.verify()

def test_getWeatherById(pact,consumer):
    expected = {
    "date": "2022-12-15",
    "temperatureC": -20,
    "temperatureF": -25,
    "summary": "Chilly"
    }

    (
        pact.given("Weather list exists in the database")
        .upon_receiving("get specific weather Item")
        .with_request("get", "/forecast/1")
        .will_respond_with(200, body=Like(expected))
    )

    with pact:
        # Perform the actual request
    
        user = consumer.get_weatherbyId(1)
        # Assert the data
        assert user['summary'] == "Chilly"

        # Make sure that all interactions defined occurred
        pact.verify()



def test_postWeatherForecast(pact):
    # Define the Matcher; the expected structure and content of the response
    expected = {
    "date": "2022-12-15",
    "temperatureC": 30,
    "temperatureF": 85,
    "summary": "Hot"
    }

    reqbody = {
    "date": "2022-12-19",
    "temperatureC": 90,
    "temperatureF": 90,
    "summary": "Red Hot"
    }

    (
        pact.given("Weather list exists in the database")
        .upon_receiving("a request to create new weather forecast")
        .with_request(
            method='POST',
            path='/forecast',
            body=reqbody)
        .will_respond_with(200, body=Like(expected))
    )

    with pact:
        # Perform the actual request
        weather = Weather(reqbody['date'], reqbody['temperatureC'], reqbody['temperatureF'], reqbody['summary'],"http://localhost:1234")
        user = weather.post_weather(reqbody)
       
        # In this case the mock Provider will have returned a valid response
        print(user)
        assert user['summary'] == "Hot"

        # Make sure that all interactions defined occurred
        pact.verify()

