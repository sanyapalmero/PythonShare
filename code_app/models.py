from user.models import User

from django.contrib import admin
from django.db import models
from django.template.defaultfilters import truncatewords
from django.utils import timezone


class Code(models.Model):
    code = models.TextField()
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(default=timezone.now, blank=False)
    date_last_change = models.DateTimeField(default=timezone.now, blank=False)
    topic = models.CharField(max_length=100, null=True)

    @property
    def short_code(self):
        return truncatewords(self.code, 4)

    @property
    def get_user(self):
        if self.user != None:
            return (self.user.username)
        else:
            return ("Unknown")


class Tag(models.Model):
    code = models.ForeignKey(Code, null=True, on_delete=models.CASCADE)
    tag = models.CharField(max_length=100, db_index=True)

    @property
    def get_code(self):
        if self.code != None:
            return (self.code.code)
        else:
            return ("Unknown")


class Comment(models.Model):
    code = models.ForeignKey(Code, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    commentary = models.CharField(max_length=500, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now, blank=False)
    reply_to = models.ForeignKey(
        "Comment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None)
