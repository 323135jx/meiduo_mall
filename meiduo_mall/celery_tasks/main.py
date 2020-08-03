from celery import Celery

# 在异步环境中加载django的环境
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','meiduo_mall.settings.dev')


# 初始化一个应用程序对象
celery_app = Celery("meiduo")

# 加载配置文件--参数是配置文件(模块)的导报路径
# 我们将来实在celery_tasks包所在的目录为工作目录运行异步程序
celery_app.config_from_object('celery_tasks.config')

celery_app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.email', 'celery_tasks.html'])