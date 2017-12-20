"""Views for django based facade"""
from enum import Enum, unique

from django.utils.decorators import method_decorator
from functools import wraps
from typing import Callable, Optional
import datetime

from newstler_site.django_facade.forms import SimpleLoginForm, RegistrationForm
from newstler_site.external_services.linkedin_client import RESTError
from newstler_site.external_services.service_registry import ServiceRegistry
from django_app.models import UserMetaInformationModel

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

STATE_SESSION_NAME = "state"


@unique
class PageName(Enum):
    HOME_PAGE = "index"
    NEWS = "news_page"
    LOGIN = "login"
    SIGN_IN = "register"
    LINKEDIN_REDIRECT_POINT = "linkedin_endpoint"


def anonymous_required(func: Callable) -> Callable:
    """Anonymous required auth helper decorator"""
    @wraps(func)
    def decorator(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated():
            return redirect(to=reverse(PageName.HOME_PAGE.value))
        return func(request, *args, **kwargs)
    return decorator


class AuthRequestHandler:
    @method_decorator(anonymous_required)
    def login_page(self, request: HttpRequest, template_name: str) -> HttpResponse:
        if request.method == "POST":
            form = SimpleLoginForm(request.POST)
            if form.is_valid():
                user = authenticate(request, email=form.cleaned_data["email"], password=form.cleaned_data["password"])
                if user:
                    login(request, user)
                    return redirect(to=request.GET.get("next", reverse(PageName.HOME_PAGE.value)))
                else:
                    form.add_error("password", "Incorrect email or password")
        else:
            form = SimpleLoginForm()
        return render(request, template_name, {"form": form})

    @method_decorator(anonymous_required)
    def register(self, request: HttpRequest, template_name: str) -> HttpResponse:
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(email=email, password=raw_password)
                login(request, user)
                return redirect(PageName.HOME_PAGE.value)
        else:
            form = RegistrationForm()
        return render(request, template_name, {"form": form})

    @method_decorator(login_required)
    def logout_page(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return redirect(reverse(PageName.LOGIN.value))


class NewstlerHandler:
    @method_decorator(login_required)
    def index(self, request: HttpRequest, template_name: str) -> HttpResponse:
        linkedin_client = ServiceRegistry.get().linkedin()
        state, endpoint = linkedin_client.authorization_endpoint
        request.session[STATE_SESSION_NAME] = state.hex
        if not hasattr(request.user, "meta") or not request.user.meta.access_token:
            return render(request, template_name, {"linkedin_auth_url": endpoint})
        else:
            return redirect(to=reverse(PageName.NEWS.value))

    @method_decorator(login_required)
    def news_page(self, request: HttpRequest, template_name: str) -> HttpResponse:
        linkedin_client = ServiceRegistry.get().linkedin()
        storage = ServiceRegistry.get().news_storage()
        with linkedin_client.session(access_token=request.user.meta.access_token) as user_session:
            try:
                user_data = user_session.get_user_data()
            except RESTError as e:
                return HttpResponse("<h1>Failed to get access token: {}".format(e.error))
            if not user_data:
                request.user.meta.access_token = None
                request.user.meta.save()
                return redirect(reverse(PageName.HOME_PAGE.value))
        news = storage.get_news_by_user_data(user_data)
        return render(request, template_name, {"news": news, "user_data": user_data})


class LinkedInHandler:
    @method_decorator(login_required)
    def linkedin_endpoint(self, request):
        auth_code = request.GET.get("code")  # type: Optional[str]
        state = request.GET.get("state")  # type: Optional[str]
        session_state = request.session.get("state")
        if not auth_code or not session_state or not state or session_state != state.strip():
            return HttpResponse("<h1>Failed process</h1><p>{}</p>".format(request.GET.get("error")))
        linkedin_client = ServiceRegistry.get().linkedin()
        access_token_data = linkedin_client.get_access_token(auth_code=auth_code)
        try:
            user_meta = UserMetaInformationModel.objects.get(user_id=request.user.id)
        except ObjectDoesNotExist:
            user_meta = UserMetaInformationModel()
            user_meta.user = request.user
        user_meta.access_token = access_token_data.access_token
        user_meta.expiration = datetime.datetime.now() + datetime.timedelta(seconds=access_token_data.expires)
        user_meta.save()

        return redirect(to=reverse(PageName.NEWS.value))
