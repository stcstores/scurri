"""The requests module provides classes for Scurri API requests."""

from typing import Any, Dict, List, Mapping, Optional

from . import exceptions
from .apisession import ScurriAPISession


class PaginatedResponse:
    """Holds response data for paginated requests."""

    COUNT = "count"
    NEXT = "next"
    PREVIOUS = "previous"
    RESULTS = "results"

    def __init__(self, kwargs: Dict[str, Any]) -> None:
        """Parse paginated request response data."""
        self.count: int = kwargs[self.COUNT]
        self.next: Optional[str] = kwargs[self.NEXT]
        self.previous: Optional[str] = kwargs[self.PREVIOUS]
        self.results: List[Dict[str, Any]] = kwargs[self.RESULTS]


class BaseRequest:
    """Base class for Scurri API requests."""

    method: str

    @classmethod
    def uri(cls, *args: List[Any], **kwargs: Dict[str, Any]) -> str:
        """Override this method to return the endpoint URI."""
        raise NotImplementedError()

    @classmethod
    def headers(cls) -> Dict[str, str]:
        """Override this method to add additional request headers."""
        return {}

    @classmethod
    def _make_request(
        cls,
        api_session: ScurriAPISession,
        method: str,
        uri: str,
        headers: Dict[str, str],
        data: Optional[Dict[str, str]],
    ) -> Dict[str, Any]:
        auth_headers = api_session.get_headers()
        request_headers = auth_headers | headers
        response = api_session.session.request(
            method=method,
            url=uri,
            headers=request_headers,
            json=data,
        )
        try:
            return dict(response.json())
        except Exception as e:
            raise exceptions.InvalidResponse(uri, response.text) from e


class SingleRequest(BaseRequest):
    """Base class for unpaginated Scurri API requests."""

    @classmethod
    def parse_response(cls, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Override this method to parse the request response."""
        return response_data

    @classmethod
    def request(
        cls,
        api_session: ScurriAPISession,
        data: Optional[Dict[str, str]] = None,
        params: Optional[Mapping] = None,
    ) -> Dict[str, Any]:
        """Make an API call."""
        if params is None:
            params = {}
        response = cls._make_request(
            api_session=api_session,
            method=cls.method,
            uri=api_session.base_url + cls.uri(**params),
            headers=cls.headers(),
            data=data,
        )
        return cls.parse_response(response)


class PaginatedRequest(BaseRequest):
    """Base class for paginated Scurri API requests."""

    @classmethod
    def request(
        cls,
        api_session: ScurriAPISession,
        data: Optional[Dict[str, str]] = None,
        params: Optional[Mapping] = None,
    ) -> List[Dict[str, Any]]:
        """Make an API call."""
        if params is None:
            params = {}
        responses = []
        uri = api_session.base_url + cls.uri(**params)
        while True:
            response = PaginatedResponse(
                cls._make_request(
                    api_session=api_session,
                    method=cls.method,
                    uri=uri,
                    headers=cls.headers(),
                    data=data,
                )
            )
            responses.append(response)
            if response.next is None:
                break
            uri = response.next
        return cls.parse_responses(responses)

    @classmethod
    def parse_responses(
        cls, responses: List[PaginatedResponse]
    ) -> List[Dict[str, Any]]:
        """Override this method to parse the request response."""
        results = []
        for response in responses:
            results.extend(response.results)
        return results


class CarriersRequest(PaginatedRequest):
    """Request a list of carriers."""

    method = "GET"

    @classmethod
    def uri(cls, *args: List[Any], **kwargs: Dict[str, Any]) -> str:
        """Return the request URI."""
        return "/carriers"


class CarrierRequest(SingleRequest):
    """Request information about a carrier."""

    @classmethod
    def uri(cls, *args: List[Any], **kwargs: Dict[str, Any]) -> str:
        """Return the request URI."""
        carrier_slug = kwargs["carrier_slug"]
        return f"/carriers/{carrier_slug}"


class CarrierTrackingsRequest(PaginatedRequest):
    """Request a tracking list for a carrier."""

    method = "GET"

    @classmethod
    def uri(cls, *args: List[Any], **kwargs: Dict[str, Any]) -> str:
        """Return the request URI."""
        carrier_slug = kwargs["carrier_slug"]
        return f"/carriers/{carrier_slug}/trackings"


class TrackingsRequest(PaginatedRequest):
    """Request a tracking list for all carriers."""

    method = "GET"

    @classmethod
    def uri(cls, *args: List[Any], **kwargs: Dict[str, Any]) -> str:
        """Return the request URI."""
        return "/trackings"


class TrackingByPackageID(SingleRequest):
    """Request tracking for a package py package ID."""

    method = "GET"

    @classmethod
    def uri(cls, *args: List[Any], **kwargs: Dict[str, Any]) -> str:
        """Return the request URI."""
        package_id = kwargs["package_id"]
        return f"/trackings/{package_id}"


class TrackingByTrackingNumber(SingleRequest):
    """Request tracking for a package py package ID."""

    method = "GET"

    @classmethod
    def uri(cls, *args: List[Any], **kwargs: Dict[str, Any]) -> str:
        """Return the request URI."""
        carrier_slug = kwargs["carrier_slug"]
        tracking_number = kwargs["tracking_number"]
        return f"/carriers/{carrier_slug}/trackings/{tracking_number}"
