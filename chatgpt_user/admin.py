from django.contrib import admin
from chatgpt_user.models import FrontUserBase, EmailVerifyCode, FrontUserExtraEmail
# Register your models here.

admin.site.register(FrontUserBase)
admin.site.register(EmailVerifyCode)
admin.site.register(FrontUserExtraEmail)