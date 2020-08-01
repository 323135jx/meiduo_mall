from django.db import models
from itsdangerous import TimedJSONWebSignatureSerializer,BadSignature
from meiduo_mall.settings import dev
# Create your models here.

from django.contrib.auth.models import AbstractUser

# 设置用户密码: AbstractUser.set_password()
# 校验密码: AbstractUser.check_password()
# Django默认给我们提供身份认证，权限检查功能
from meiduo_mall.utils.BaseModel import BaseModel


class User(AbstractUser):

    # 补充字段： mobile
    mobile = models.CharField(
        unique=True,
        verbose_name='手机号',
        null=True,
        max_length=11

    )
    email_active = models.BooleanField(
        default=False,
        verbose_name="邮箱验证状态"
    )
    default_address = models.ForeignKey('Address',
                                        related_name='users',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL,
                                        verbose_name='默认地址'
                                        )

    class Meta:
        db_table = 'tb_user'    # 制定模型类User所映射的mysql表明
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


    # 用户模型中封装该方法
    def generate_verify_email_url(self):
        """
        生成当前用户的令牌；并且拼接邮箱确认的连接；
        :return: 返回确认连接
        """
        serializer = TimedJSONWebSignatureSerializer(secret_key=dev.SECRET_KEY)

        user_info = {'user_id':self.id, 'email':self.email}

        token = serializer.dumps(user_info)

        verify_url = dev.EMAIL_VERIFY_URL + token.decode()

        return verify_url


    # 校验token值，返回用户对象
    @staticmethod
    def check_verify_email_token(token):
        """
        校验token值
        :param token: token值
        :return: 用户对象 或 None
        """
        serializer = TimedJSONWebSignatureSerializer(secret_key=dev.SECRET_KEY)

        try:
            user_info = serializer.loads(token)
        except BadSignature as e:
            print(e)
            return None

        user_id = user_info.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist as e:
            print(e)
            return None

        return user

class Address(BaseModel):
    """用户地址"""
    user = models.ForeignKey(User,
                             on_delete = models.CASCADE,
                             related_name = 'addresses',
                             verbose_name='用户'
                             )
    province = models.ForeignKey('areas.Area',
                         on_delete = models.PROTECT,
                         related_name = 'province_addresses',
                         verbose_name='省'
                         )
    city = models.ForeignKey('areas.Area',
                         on_delete = models.PROTECT,
                         related_name = 'city_addresses',
                         verbose_name='市'
                         )
    district = models.ForeignKey('areas.Area',
                         on_delete = models.PROTECT,
                         related_name = 'district_addresses',
                         verbose_name='区'
                         )

    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20,
                           null=True,
                           blank=True,
                           default='',
                           verbose_name='固定电话')
    email = models.CharField(max_length=30,
                           null=True,
                           blank=True,
                           default='',
                           verbose_name='电子邮箱')

    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_addresses'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name

        # 定义默认查询集排序方式
        ordering = ['-update_time']




