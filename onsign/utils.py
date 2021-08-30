from django.conf import settings
from decimal import Decimal, ROUND_HALF_UP
import requests

from onsign.constants import HTTP_X_FORWARDED_FOR, REMOTE_ADDR
from onsign.exceptions import GoogleZeroResults, DarkSkyZeroResults


def get_client_ip(request):
    x_forwarded_for = request.META.get(HTTP_X_FORWARDED_FOR)
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get(REMOTE_ADDR)


def round(decimal, precision):
    if not isinstance(decimal, Decimal):
        decimal = Decimal(decimal)
    return decimal.quantize(Decimal(precision), ROUND_HALF_UP)


class GoogleAPI(object):
    def __init__(self, term):
        self.google_url = '{google_api_url}?address={address}&key={google_key}'.format(
            google_api_url=settings.GOOGLE_API_URL, address=term, google_key=settings.GOOGLE_API_KEY
        )
        self.data = self.get_data()

    def raise_exception(self):
        raise GoogleZeroResults('No results was found with the given address')

    def get_data(self):
        response = requests.get(url=self.google_url, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return response.json()

    def get_lat_lng(self):
        results = self.data.get('results')
        if results:
            location = results[0]['geometry']['location']
            return location['lat'], location['lng']
        self.raise_exception()

    def get_long_name(self):
        results = self.data.get('results')
        if results:
            return results[0]['address_components'][0]['long_name']
        self.raise_exception()


class DarkSkyAPI(object):
    def __init__(self, latitude, longitude):
        self.darksky_url = '{darksky_api_url}/{darksky_key}/{latitude},{longitude}?units=si'.format(
            darksky_api_url=settings.DARKSKY_API_URL, darksky_key=settings.DARKSKY_API_KEY,
            latitude=latitude, longitude=longitude
        )
        self.data = self.get_data()

    def raise_exception(self):
        raise DarkSkyZeroResults('No results was found with the given lat/lng')

    def get_data(self):
        response = requests.get(url=self.darksky_url, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return response.json()

    def get_current_temperature(self):
        results = self.data.get('currently')
        if results:
            return results['temperature']
        self.raise_exception()
