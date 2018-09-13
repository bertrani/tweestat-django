from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views

iso8601_pattern = "([0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9])"

urlpatterns = [
    path('', TemplateView.as_view(template_name='stats/form.html'), name='index'),
    path('redirect', views.stat, name='stats'),
    re_path(r'^mean/(?P<field>\w+)/(?P<start>{})/(?P<end>{})/$'.format(iso8601_pattern, iso8601_pattern), views.mean)
]
