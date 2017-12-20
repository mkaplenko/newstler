from django.db import models
from django.contrib.auth.models import User


class UserMetaInformationModel(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="meta")
    access_token = models.TextField(verbose_name="linkedIn access token", null=True, blank=True)
    expiration = models.DateTimeField(verbose_name="Token expiration", null=True, blank=True)

    def __str__(self):
        return self.user.username


class NewsTag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class NewsItem(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=100)
    tag = models.ForeignKey(to=NewsTag, related_name="news")

    def __str__(self):
        return self.title
