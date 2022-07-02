from django.contrib import admin
from .models import User, UserLog, UserSetting

admin.site.register(User)
admin.site.register(UserSetting)
admin.site.register(UserLog)

