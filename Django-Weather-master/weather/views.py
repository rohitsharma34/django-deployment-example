# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from weather.models import City
from weather.service import weather_by_city_id


class HomeView(TemplateView):
    template_name = 'weather/home.html'


class CitySearchListView(ListView):
    model = City
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        try:
            return super(CitySearchListView, self).get(request, *args, **kwargs)
        except Http404:
            response = redirect('weather:search_results')
            params = '?q={q};page={page}'.format(q=request.GET.get('q'), page=1)
            response['Location'] += params
            return response

    def get_queryset(self):
        city_name = self.request.GET.get('q')
        return self.model.objects.filter(name__istartswith=city_name)\
                                 .extra(select={'length': 'length(name)'})\
                                 .order_by('length', 'country_id')

    def get_context_data(self, **kwargs):
        context = super(CitySearchListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')


        return context




class CityWeatherView(TemplateView):
    template_name = 'weather/city_weather.html'
    partial_template_name = 'weather/city_weather_partial.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():

            return render(request, self.partial_template_name, self.get_context_data(**kwargs))
        return super(CityWeatherView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CityWeatherView, self).get_context_data(**kwargs)
        context['city_weather'] = weather_by_city_id(self.kwargs['city_id'])
        context['city_id'] = self.kwargs['city_id']
        return context
