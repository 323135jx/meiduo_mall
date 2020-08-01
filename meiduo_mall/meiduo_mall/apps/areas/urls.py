from areas.views import *
from django.urls import re_path

urlpatterns = [
    re_path(r'^areas/$', ProvinceAreasView.as_view()),
    re_path(r'^areas/(?P<pk>[1-9]\d+)/$', SubAreasView.as_view()),
]