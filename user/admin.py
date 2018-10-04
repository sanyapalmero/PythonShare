from django.contrib import admin
from .models import User


@admin.register(User)
class TextAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_full_name', 'is_staff')
