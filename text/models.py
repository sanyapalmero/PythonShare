from django.db import models
from django.contrib import admin
from django.template.defaultfilters import truncatewords


class Text(models.Model):
    text = models.CharField(max_length=100)

    @property
    def short_text(self):
        return truncatewords(self.text, 4)


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_text')
