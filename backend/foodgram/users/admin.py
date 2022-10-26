from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'first_name')


admin.site.register(User, UserAdmin)
