from django.contrib import admin
from .models import Text


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_text', 'get_user')
