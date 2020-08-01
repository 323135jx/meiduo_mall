from django.contrib.auth.backends import ModelBackend
from .models import User
from django.http import JsonResponse

class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self,request,username=None,password=None, **kwargs):
        # 1.接受数据
        try:
            user = User.objects.get(username=username)
        except:
            try:
                user = User.objects.get(mobile=username)
            except:
                pass
        else:
            if user.check_password(password)and self.user_can_authenticate(user):
                return user

        # 2.处理数据
        # 3.用户认证
        # 返回数据