# from django.contrib import admin
# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import CustomUser, EmailVerifyRecord
#
#
# class CustomInline(admin.StackedInline):
#     model = CustomUser
#     can_delete = False
#
#
# class UserAdmin(BaseUserAdmin):
#     inlines = (CustomInline, )
#     list_display = ['username', 'nickname', 'is_staff', 'is_active', 'is_superuser']
#
#     def nickname(self):
#         return self.obj.customuser.nickname
#
#     nickname.short_description = '昵称'
#
#
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
#
#
# @admin.register(CustomUser)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ['user', 'nickname']
#
#
# @admin.register(EmailVerifyRecord)
# class EmailVerifyRecordAdmin(admin.ModelAdmin):
#     list_display = ['code', 'email', 'send_type', 'send_time']
