"""LinkedIn service client implementation"""
from abc import ABC, abstractmethod
from collections import namedtuple
from contextlib import contextmanager
from typing import Tuple, ContextManager, Optional, Sequence
from uuid import uuid4, UUID
from http.server import HTTPStatus

from yarl import URL
import requests


UserData = namedtuple("UserData", ("name", "position"))
AccessTokenResponse = namedtuple("AccessTokenResponse", ("access_token", "expires"))


class LinkedInClient(ABC):
    @abstractmethod
    def authorization_endpoint(self) -> Tuple[UUID, URL]:
        """LinkedIn state and endpoint for getting user OAuth2.0 authorization code"""

    @abstractmethod
    def get_access_token(self, auth_code: str) -> AccessTokenResponse:
        """Get user access token by auth code"""

    @abstractmethod
    def get_user_data(self) -> Optional[UserData]:
        """Get user data"""

    @abstractmethod
    def session(self, access_token: str) -> ContextManager["LinkedInClient"]:
        """Get user authenticated linkedin session"""


class FakeLinkedInClient(LinkedInClient):
    # Main idea of fake service classes is to provide API support for developers (this is not mock for tests)
    # if there are no access to
    # real service by any reasons (usually we don't need real access for developing).
    # In that test case not fully implement (no facade support, in case time limit), but added for idea demonstration.
    def authorization_endpoint(self) -> Tuple[str, URL]:
        return uuid4(), URL("http://fakelinkedin.com/authorize")

    def get_access_token(self, auth_code: str) -> AccessTokenResponse:
        return AccessTokenResponse(access_token=uuid4().hex, expires="11260")

    def get_user_data(self) -> Optional[UserData]:
        return UserData(name="Fake User", position="JavaScript Developer")

    @contextmanager
    def session(self, access_token: str) -> ContextManager[LinkedInClient]:
        yield self


class RESTError(Exception):
    def __init__(self, error: str, *args):
        super(RESTError, self).__init__(error, *args)
        self.error = error


class RestLinkedInClient(LinkedInClient):
    """LinkedIn REST client"""
    def __init__(self, *, base_url: str, client_id: str, client_secret: str, redirect_uri: str, auth_path: str,
                 token_path: str, api_url: str):
        self.api_url = api_url
        self.token_path = token_path
        self.auth_path = auth_path
        self.redirect_uri = redirect_uri
        self.base_url = base_url
        self.client_secret = client_secret
        self.client_id = client_id
        self.__user_access_token = None

    @property
    def authorization_endpoint(self) -> Tuple[UUID, URL]:
        state = uuid4()
        return state, URL(self.base_url).with_path(self.auth_path).with_query(
            response_type="code",
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            state=state.hex,
        )

    @staticmethod
    def __validate_response(response: requests.Response, expected_codes: Sequence[HTTPStatus]):
        if response.status_code not in (code.value for code in expected_codes):
            raise RESTError("Unexpected response code [{}] from linkedin client, expected: [{}]".format(
                response.status_code, expected_codes))

    def get_access_token(self, auth_code: str) -> AccessTokenResponse:
        url = URL(self.base_url).with_path(self.token_path)
        data = dict(grant_type="authorization_code",
                    code=auth_code,
                    redirect_uri=self.redirect_uri,
                    client_id=self.client_id,
                    client_secret=self.client_secret)
        response = requests.post(url=str(url), data=data)
        self.__validate_response(response, expected_codes=[HTTPStatus.OK])
        if response.status_code == HTTPStatus.BAD_REQUEST:
            raise RESTError(response.json()["error"])
        return AccessTokenResponse(access_token=response.json()["access_token"], expires=response.json()["expires_in"])

    @contextmanager
    def session(self, access_token: str) -> ContextManager[LinkedInClient]:
        new_instance = self.__class__(
            base_url=self.base_url,
            client_secret=self.client_secret,
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            token_path=self.token_path,
            auth_path=self.auth_path,
            api_url=self.api_url,
        )  # type: LinkedInClient
        new_instance.__user_access_token = access_token
        yield new_instance
        del new_instance

    def get_user_data(self) -> Optional[UserData]:
        if not self.__user_access_token:
            raise ValueError("LinkedIn session does not initialized by user access token")
        url = URL(self.base_url).with_path("/v1/people/~:(first-name,positions)").with_query(format="json")
        response = requests.get(str(url), headers={"Authorization": "Bearer {}".format(self.__user_access_token)})
        self.__validate_response(response, expected_codes=[HTTPStatus.OK, HTTPStatus.FORBIDDEN,
                                                           HTTPStatus.UNAUTHORIZED])
        if response.status_code == HTTPStatus.FORBIDDEN or response.status_code == HTTPStatus.UNAUTHORIZED:
            return None
        data = response.json()
        if data["positions"]["values"]:
            position = next(iter(data["positions"]["values"]))["title"]
        else:
            position = None
        return UserData(name=data["firstName"], position=position)
