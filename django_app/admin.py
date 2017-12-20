from django.contrib import admin
from django_app.models import UserMetaInformationModel, NewsItem, NewsTag

# Register your models here.

admin.site.register(UserMetaInformationModel)
admin.site.register(NewsItem)
admin.site.register(NewsTag)
