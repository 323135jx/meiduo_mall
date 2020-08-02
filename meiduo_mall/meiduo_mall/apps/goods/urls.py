from django.urls import re_path
from .views import *

urlpatterns = [
    re_path(r"^list/(?P<category_id>\d+)/skus/$",ListView.as_view()),

    re_path(r"^hot/(?P<category_id>\d+)/$", HotGoodsView.as_view()),
    re_path(r"^search/$", MySerachView()),


]