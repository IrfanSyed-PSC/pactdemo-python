from typing import Optional

import requests
from datetime import datetime


class Weather(object):
    """Define the basic User data we expect to receive from the User Provider."""

    def __init__(self, date: str, temperatureC: int, temperatureF: int, summary: str, base_uri: str):
        self.date = date
        self.temperatureC = temperatureC
        self.temperatureF = temperatureF
        self.summary = summary
        self.base_uri = base_uri

    def post_weather(self, body: object):
        uri = self.base_uri + "/forecast"
        body = {
            "date": self.date,
            "temperatureC": self.temperatureC,
            "temperatureF": self.temperatureF,
            "summary": self.summary
        }

        response = requests.post(uri, json = body)
        if response.status_code == 404:
            return None

        return response.json()
      

class WeatherConsumer(object):
    """Demonstrate some basic functionality of how the User Consumer will interact
    with the User Provider, in this case a simple get_user."""

    def __init__(self, base_uri: str):
        """Initialise the Consumer, in this case we o   nly need to know the URI.

        :param base_uri: The full URI, including port of the Provider to connect to
        """
        self.base_uri = base_uri

    def get_weather(self) -> Optional[Weather]:
        """Fetch a user object by user_name from the server.

        :param user_name: User name to search for
        :return: User details if found, None if not found
        """
        uri = self.base_uri + "/forecast"
        response = requests.get(uri)
        if response.status_code == 404:
            return None

        return response.json()

    def get_news(self) -> Optional[Weather]:
       
        uri = self.base_uri + "/forecast"
        response = requests.get(uri)
        if response.status_code == 404:
            return None

        return response.json()    

    def get_dailynews(self) -> Optional[Weather]:
       
        uri = self.base_uri + "/forecast"
        response = requests.get(uri)
        if response.status_code == 404:
            return None

        return response.json()  

    def get_livenews(self) -> Optional[Weather]:
       
        uri = self.base_uri + "/forecast"
        response = requests.get(uri)
        if response.status_code == 404:
            return None

        return response.json() 
       
    def get_weatherbyId(self, Id: str) -> Optional[Weather]:
        """Fetch a user object by user_name from the server.

        :param user_name: User name to search for
        :return: User details if found, None if not found
        """
        uri = self.base_uri + "/forecast/" + str(Id)
        response = requests.get(uri)
        if response.status_code == 404:
            return None

        return response.json()
        # summary = response.json()["summary"]
        # date = datetime.strptime(response.json()["created_on"], "%Y-%m-%dT%H:%M:%S")

        # return User(summary, date)
