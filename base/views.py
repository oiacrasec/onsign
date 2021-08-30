# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View


# class HomePageView(TemplateView):
#     template_name = 'pages/index/index.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(HomePageView, self).get_context_data(**kwargs)
#         # Extra context can be implemented here
#         return context


class HomePageView(View):
    """
    Redirecting to temperature info without affect index.
    We can create a isolated index after, using code above.
    """

    def get(self, request):
        return redirect(reverse('temperature-info'))
