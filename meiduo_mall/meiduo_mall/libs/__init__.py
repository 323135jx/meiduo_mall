# 导入
from meiduo_mall.libs.captcha.captcha import captcha

# 调用对象的函数, 生成图片 image 和 对应的内容 text
text, image = captcha.generate_captcha()
