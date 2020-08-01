
from django.core.mail import send_mail
# from django.conf import settings
from meiduo_mall.settings import dev

from celery_tasks.main import celery_app

@celery_app.task(name='send_verify_email')
def send_verify_email(to_email, verify_url):
    subject = '美多邮箱验证码'

    html_message = '<p>劳模版的卧底您好！</p>'\
                   '<p>感谢您使用我们的美多商城</p>'\
                   '<p>您的联络密码为：%s。 请点击此链接激活您的邮箱：</p>'\
                   '<p><a href="%s">%s</a></p>'%(to_email, verify_url, verify_url)
    send_mail(
        subject,
        '',
        dev.EMAIL_FROM,
        [to_email],
        html_message=html_message
    )

