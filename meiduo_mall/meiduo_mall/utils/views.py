from django.http import JsonResponse

# 定义一个装饰器，验证是否登录
def login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return JsonResponse({
                'code':400,
                'errmsg':'您未登录'
            })
    return wrapper