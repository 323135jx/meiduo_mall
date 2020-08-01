from celery_tasks.main import celery_app
from celery_tasks.yuntongxun.ccp_sms import CCP


@celery_app.task(name='ccp_send_sms_code')
def ccp_send_sms_code(mobile, sms_code):
    # CCP().send_tampalate_sms()...
    print(sms_code)
    return CCP().send_template_sms(mobile, [sms_code,5], 1)