"""newstler_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from newstler_site.django_facade import handlers

from django.conf.urls import url
from django.contrib import admin

auth_handler = handlers.AuthRequestHandler()
linkedin_handler = handlers.LinkedInHandler()
main_handler = handlers.NewstlerHandler()

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^login/$", auth_handler.login_page, {"template_name": "login.html"}, name=handlers.PageName.LOGIN.value),
    url(r"^logout/$", auth_handler.logout_page, name="logout"),
    url(r"^signup/$", auth_handler.register, {"template_name": "register.html"}, name=handlers.PageName.SIGN_IN.value),
    url(r"^linkedin/$", linkedin_handler.linkedin_endpoint, name=handlers.PageName.LINKEDIN_REDIRECT_POINT.value),
    url(r"^news/$", main_handler.news_page, {"template_name": "news.html"}, name=handlers.PageName.NEWS.value),
    url(r"^$", main_handler.index, {"template_name": "linkedin.html"}, name=handlers.PageName.HOME_PAGE.value),
]
