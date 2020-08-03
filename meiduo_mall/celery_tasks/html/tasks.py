import os
from django.conf import  settings
from django.template import  loader
# from goods.utils import  import
from celery_tasks.main import celery_app


# @app.task(name='generate_static')