from django.db import models
from django.contrib import admin
from django.template.defaultfilters import truncatewords
from django.utils import timezone
from user.models import User


class Text(models.Model):
    text = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, blank=True)

    @property
    def short_text(self):
        return truncatewords(self.text, 4)

    @property
    def get_user(self):
        if self.user != None:
            return (self.user.username)
        else:
            return ("Unknown")


class Tag(models.Model):
    text = models.ForeignKey(Text, null=True, on_delete=models.CASCADE)
    tag = models.CharField(max_length=100, db_index=True)

    @property
    def get_tag(self):
        return (self.tag)

    @property
    def get_code(self):
        if self.text != None:
            return (self.text.text)
        else:
            return ("Unknown")
