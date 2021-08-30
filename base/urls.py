from django.urls import path

from base.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
]
