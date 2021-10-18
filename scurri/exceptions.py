"""Exceptions for the scurri package."""


class NotAuthorizedException(Exception):
    """Exception raised when attempting a request before authorising."""

    def __init__(self) -> None:
        """Exception raised when attempting a request before authorising."""
        super().__init__("Current session is not authorized.")


class InvalidResponse(ValueError):
    """Exception raised when a request returns an invalid response."""

    def __init__(self, uri: str, response: str):
        """Exception raised when a request returns an invalid response."""
        super().__init__(f"Invalid response from '{uri}': '{response}'.")


class InvalidAuthRequestResponse(ValueError):
    """Exception raised when authorisation returns an invalid response."""

    def __init__(self, response_text: str) -> None:
        """Exception raised when authorisation returns an invalid response."""
        super().__init__(f"Invalid response from auth request: {response_text}.")


class BaseNotFoundError(ValueError):
    """Base exception for requests that do not find what they are looking for."""

    pass


class CarrierNotFound(BaseNotFoundError):
    """Exception raised when requesting a carrier that does not exist."""

    def __init__(self, carrier_slug: str):
        """Exception raised when requesting a carrier that does not exist."""
        super().__init__(f'No carrier found with slug "{carrier_slug}".')


class PackageNotFound(BaseNotFoundError):
    """Exception raised when requesting a package that does not exist."""

    pass


class TooManyRequestsError(Exception):
    """Exception raised when a paginated request has requested many pages."""

    def __init__(self) -> None:
        """Exception raised when a paginated request has requested many pages."""
        super().__init__("Too many pages requested.")


class TooManyRequestAtemptsError(Exception):
    """Exception raised when an API request fails too many times."""

    def __init__(self, uri: str) -> None:
        """Exception raised when an API request fails too many times."""
        super().__init__(f'Too many failed requests to "{uri}".')
