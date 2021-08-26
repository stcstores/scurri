import pytest

from scurri import ScurriAPISession, exceptions


@pytest.fixture
def scurri_api():
    return ScurriAPISession()


@pytest.fixture
def auth_endpoint_url(scurri_api):
    return f"{scurri_api.base_url}{scurri_api.AUTH_URI}"


@pytest.fixture
def mock_auth_endpoint(requests_mock, auth_endpoint_url, token):
    requests_mock.post(auth_endpoint_url, json={"token": token})


@pytest.fixture
def mock_auth_endpoint_with_invalid_credentials(requests_mock, auth_endpoint_url):
    requests_mock.post(
        auth_endpoint_url,
        json={"non_field_errors": ["Unable to log in with provided credentials."]},
    )


@pytest.fixture
def completed_auth_request(scurri_api, mock_auth_endpoint, username, password):
    scurri_api.auth(username=username, password=password)


def test_using_live_url():
    assert ScurriAPISession(staging=False).base_url == ScurriAPISession.LIVE_URL


def test_using_staging_url():
    assert ScurriAPISession(staging=True).base_url == ScurriAPISession.STAGING_URL


def test_auth_method_sends_login_information(
    requests_mock, username, password, completed_auth_request
):
    request = requests_mock.request_history[0]
    assert request.json() == {"username": username, "password": password}


def test_auth_method_makes_one_call(requests_mock, completed_auth_request):
    assert requests_mock.call_count == 1


def test_auth_method_calls_auth_endpoint(
    requests_mock, auth_endpoint_url, completed_auth_request
):
    request = requests_mock.request_history[0]
    assert request.url == auth_endpoint_url


def test_auth_method_sets_token(scurri_api, token, completed_auth_request):
    assert scurri_api.token == token


def test_get_headers_method(scurri_api, token, completed_auth_request):
    assert scurri_api.get_headers() == {"Authorization": f"Token {token}"}


def test_get_headers_method_without_auth(scurri_api):
    with pytest.raises(exceptions.NotAuthorizedException):
        scurri_api.get_headers()


def test_failed_authorization(
    mock_auth_endpoint_with_invalid_credentials, scurri_api, username, password
):
    with pytest.raises(exceptions.InvalidAuthRequestResponse):
        scurri_api.auth(username=username, password=password)


def test_failed_authorization_does_not_set_token(
    mock_auth_endpoint_with_invalid_credentials, scurri_api, username, password
):
    with pytest.raises(exceptions.InvalidAuthRequestResponse):
        scurri_api.auth(username=username, password=password)
    assert scurri_api.token is None
