from django.contrib.auth.backends import ModelBackend
from .models import User
from django.http import JsonResponse

class UsernameMobileAuthBackend(ModelBackend):
    # def authenticate(self,request,username=None,password=None, **kwargs):
    #     # 1.接受数据
    #     try:
    #         user = User.objects.get(username=username)
    #     except:
    #         try:
    #             user = User.objects.get(mobile=username)
    #         except:
    #             pass
    #     else:
    #         if user.check_password(password)and self.user_can_authenticate(user):
    #             return user

        # 2.处理数据
        # 3.用户认证
        # 返回数据
    def authenticate(self, request, username=None, password=None, **kwargs):
        # request: 请求对象
        # username: 用户名或手机号
        # password: 密码

        # 1、根据用户名过滤
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as e:
            # 2、根据手机号过滤
            try:
                user = User.objects.get(mobile=username)
            except User.DoesNotExist as e:
                return None

        # 3、其中某一个过滤出用户，再校验密码
        if user.check_password(password):
            return user