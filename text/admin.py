from django.contrib import admin
from .models import Text, Tag


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_text', 'get_user')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_tag', 'get_code')
