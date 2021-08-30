# -*- coding: utf-8 -*-
from urllib.parse import urlencode, quote_plus
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import CreateView
from requests import HTTPError

from onsign.exceptions import GoogleZeroResults, DarkSkyZeroResults
from onsign.utils import get_client_ip, round, GoogleAPI, DarkSkyAPI

from .forms import TrackerForm


class TrackerCreateView(CreateView):
    template_name = 'pages/temperature_location/temperature_location.html'
    form_class = TrackerForm

    def get_success_url(self):
        return reverse('temperature-info')

    def form_valid(self, form):
        error = False
        latitude = longitude = ''
        try:
            google = GoogleAPI(form.instance.location)
            latitude, longitude = google.get_lat_lng()
            longname = google.get_long_name()

            darksky = DarkSkyAPI(round(latitude, '.001'), round(longitude, '.001'))
            temperature = darksky.get_current_temperature()

            messages.info(
                self.request,
                'Temperature at <i>{locale}</i> is <span class="temperature">{temperature}°C</span>'.format(
                    locale=longname, temperature=temperature
                )
            )
        except (GoogleZeroResults, DarkSkyZeroResults) as e:
            messages.error(self.request, str(e))
            error = True
        except HTTPError:
            messages.error(self.request, 'HTTP error')
            error = True
        finally:
            form.instance.ip_address = get_client_ip(self.request)
            if error:
                form.instance.consulted = False
            form.save()
        return redirect(
            '{url}?{params}'.format(
                url=self.get_success_url(),
                params=urlencode({'lat': latitude, 'lng': longitude}, quote_via=quote_plus)
            )
        )

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TrackerCreateView, self).dispatch(request, *args, **kwargs)
