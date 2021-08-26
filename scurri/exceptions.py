class NotAuthorizedException(Exception):
    def __init__(self) -> None:
        super().__init__("Current session is not authorized.")


class InvalidAuthRequestResponse(Exception):
    def __init__(self, response_text: str) -> None:
        super().__init__(f"Invalid response from auth request: {response_text}")


class InvalidResponse(Exception):
    def __init__(self, uri: str, response: str):
        super().__init__(f"Invalid response from '{uri}': '{response}'")
