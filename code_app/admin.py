from django.contrib import admin

from .models import Code, Comment, Tag


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_code', 'get_user', 'date_creation',
                    'date_last_change')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'get_code')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'commentary', 'user', 'code')
