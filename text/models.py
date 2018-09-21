from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatewords


class Text(models.Model):
    text = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)

    @property
    def short_text(self):
        return truncatewords(self.text, 4)

    @property
    def get_user(self):
        if self.user != None:
            return (self.user.username)
        else:
            return ("Unknown")
