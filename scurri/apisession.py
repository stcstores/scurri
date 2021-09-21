"""The ScurriAPISession class."""

import json
from typing import Dict, Optional

import requests

from . import exceptions


class ScurriAPISession:
    """The ScurriAPISession class provides a Scurri API session."""

    STAGING_URL: str = "https://tracking-staging.scurri.co.uk/api/v1"
    LIVE_URL: str = "https://tracking.scurri.co.uk/api/v1"

    AUTH_URI: str = "/authorizations"
    TRACKINGS_URI: str = "/trackings"
    CARRIERS_URI: str = "/carriers"

    def __init__(self, staging: bool = False) -> None:
        """Create a scurri API session."""
        if staging is True:
            self.base_url = self.STAGING_URL
        else:
            self.base_url = self.LIVE_URL
        self.token: Optional[str] = None
        self.session: requests.Session = requests.Session()

    def auth(self, username: str, password: str) -> None:
        """
        Make a request to the authorizations endpoint to get an authorisation token.

        Kwargs:
            username (str): Your scurri username.
            password (str): Your scurri password.
        """
        self._get_token(username=username, password=password)

    def _get_token(self, username: str, password: str) -> None:
        """Request an authorisation token."""
        url = f"{self.base_url}{self.AUTH_URI}"
        request_json = {"username": username, "password": password}
        response = self.session.post(url, json=request_json)
        try:
            self.token = response.json()["token"]
        except (json.JSONDecodeError, KeyError):
            raise exceptions.InvalidAuthRequestResponse(response.text)

    def get_headers(self) -> Dict[str, str]:
        """Return auth headers for requests."""
        if self.token is None:
            raise exceptions.NotAuthorizedException()
        return {"Authorization": f"Token {self.token}"}
