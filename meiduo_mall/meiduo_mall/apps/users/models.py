from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

# 设置用户密码: AbstractUser.set_password()
# 校验密码: AbstractUser.check_password()
# Django默认给我们提供身份认证，权限检查功能

class User(AbstractUser):

    # 补充字段： mobile
    mobile = models.CharField(
        unique=True,
        verbose_name='手机号',
        null=True,
        max_length=11

    )

    class Meta:
        db_table = 'tb_user'    # 制定模型类User所映射的mysql表明
        verbose_name = '手机号'
        verbose_name_plural = '手机号'

    def __str__(self):
        return self.username