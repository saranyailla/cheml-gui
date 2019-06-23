from django.contrib import admin
from django.urls import path,include,re_path
from visualisation import views
from django.views.generic import TemplateView
urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('line', TemplateView.as_view(template_name='line.html')),
    re_path(r'^statistics',views.statistics)
]

