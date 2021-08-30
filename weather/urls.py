from django.urls import path

from .views import TrackerCreateView

urlpatterns = [
    path('temperature-info', TrackerCreateView.as_view(), name='temperature-info'),
]
