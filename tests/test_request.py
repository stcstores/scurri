from unittest.mock import MagicMock, call

import pytest

from scurri import exceptions
from scurri.request import (
    BaseRequest,
    CarrierRequest,
    CarriersRequest,
    CarrierTrackingsRequest,
    PaginatedRequest,
    PaginatedResponse,
    SingleRequest,
    TrackingByPackageID,
    TrackingByTrackingNumber,
    TrackingsRequest,
)

GET = "GET"
POST = "POST"


@pytest.fixture
def mock_uri():
    return "/mock_uri"


@pytest.fixture
def mock_headers():
    return {"mock": "headers"}


@pytest.fixture
def mock_data():
    return {"mock": "data"}


@pytest.fixture
def mock_response_data():
    return {
        "count": 3,
        "next": "https://next-url",
        "previous": "https://previous-url",
        "results": [
            {"name": "Result 1"},
            {"name": "Result 2"},
            {"name": "Result 3"},
        ],
    }


@pytest.fixture
def mock_single_request_subclass(mock_uri, mock_headers, mock_data):
    class MockSingleRequestSubclass(SingleRequest):
        method = POST

        uri = MagicMock(return_value=mock_uri)

        @classmethod
        def headers(cls):
            return mock_headers

    return MockSingleRequestSubclass


@pytest.fixture
def mock_paginated_request_subclass(mock_uri, mock_headers, mock_data):
    class MockPaginatedRequestSubclass(PaginatedRequest):
        method = GET

        uri = MagicMock(return_value=mock_uri)

        @classmethod
        def headers(cls):
            return {}

    return MockPaginatedRequestSubclass


@pytest.fixture
def mock_request_response(mock_response_data):
    mock_json = MagicMock(return_value=mock_response_data)
    mock_response = MagicMock()
    mock_response.attach_mock(mock_json, "json")
    return mock_response


def test_scurri_response_sets_count(mock_response_data):
    assert PaginatedResponse(mock_response_data).count == mock_response_data["count"]


def test_scurri_response_sets_next(mock_response_data):
    assert PaginatedResponse(mock_response_data).next == mock_response_data["next"]


def test_scurri_response_sets_previous(mock_response_data):
    assert (
        PaginatedResponse(mock_response_data).previous == mock_response_data["previous"]
    )


def test_scurri_response_sets_results(mock_response_data):
    assert (
        PaginatedResponse(mock_response_data).results == mock_response_data["results"]
    )


def test_base_request_uri_method(authenticated_scurri_api):
    with pytest.raises(NotImplementedError):
        assert BaseRequest().uri() is None


def test_base_request_headers_method(authenticated_scurri_api):
    assert BaseRequest().headers() == {}


def test_make_request_method(
    authenticated_scurri_api,
    mock_uri,
    mock_headers,
    mock_data,
    mock_request_response,
    mock_response_data,
):
    mock_request = MagicMock(return_value=mock_request_response)
    authenticated_scurri_api.session.request = mock_request
    request = BaseRequest()
    response = request._make_request(
        api_session=authenticated_scurri_api,
        method=GET,
        uri=mock_uri,
        headers=mock_headers,
        data=mock_data,
    )
    mock_request.assert_called_once_with(
        method=GET,
        url=mock_uri,
        headers=authenticated_scurri_api.get_headers() | mock_headers,
        json=mock_data,
    )
    assert isinstance(response, dict)
    mock_request_response.json.assert_called_once_with()


def test_make_request_method_with_request_error(
    authenticated_scurri_api, mock_uri, mock_headers, mock_data
):
    mock_response = MagicMock(json=MagicMock(side_effect=Exception()))
    authenticated_scurri_api.session.request = MagicMock(return_value=mock_response)
    authenticated_scurri_api.session.request
    request = BaseRequest()
    with pytest.raises(exceptions.InvalidResponse):
        request._make_request(
            api_session=authenticated_scurri_api,
            method=GET,
            uri=mock_uri,
            headers=mock_headers,
            data=mock_data,
        )


def test_single_request_request_parse_response_method(
    authenticated_scurri_api, mock_response_data
):
    response = mock_response_data
    assert SingleRequest().parse_response(response) == response


@pytest.fixture
def mock_make_request_response(mock_response_data):
    return PaginatedResponse(mock_response_data)


@pytest.fixture
def single_request_subclass_mocked_for_request_method(
    mock_single_request_subclass, mock_make_request_response
):
    mock_single_request_subclass._make_request = MagicMock(
        return_value=mock_make_request_response
    )
    mock_single_request_subclass.parse_response = MagicMock()
    return mock_single_request_subclass


@pytest.fixture
def paginated_request_subclass_mocked_for_request_method(
    mock_paginated_request_subclass, carriers_response_data
):
    mock_paginated_request_subclass._make_request = MagicMock(
        return_value=carriers_response_data[1]
    )
    mock_paginated_request_subclass.parse_response = MagicMock()
    return mock_paginated_request_subclass


def test_request_method_calls_make_request(
    single_request_subclass_mocked_for_request_method,
    authenticated_scurri_api,
    mock_uri,
    mock_headers,
    mock_data,
):

    single_request_subclass_mocked_for_request_method.request(
        api_session=authenticated_scurri_api, data=mock_data
    )
    single_request_subclass_mocked_for_request_method._make_request.assert_called_once_with(
        api_session=authenticated_scurri_api,
        method=POST,
        uri=authenticated_scurri_api.base_url + mock_uri,
        headers=mock_headers,
        data=mock_data,
    )


def test_request_method_calls_parse_response(
    single_request_subclass_mocked_for_request_method,
    authenticated_scurri_api,
    mock_make_request_response,
    mock_data,
):
    single_request_subclass_mocked_for_request_method.request(
        api_session=authenticated_scurri_api, data=mock_data
    )

    single_request_subclass_mocked_for_request_method.parse_response.assert_called_once_with(
        mock_make_request_response
    )


def test_single_request_request_method_with_params(
    authenticated_scurri_api,
    single_request_subclass_mocked_for_request_method,
    mock_data,
):
    params = {"key": "value"}
    single_request_subclass_mocked_for_request_method.request(
        api_session=authenticated_scurri_api, data=mock_data, params=params
    )
    single_request_subclass_mocked_for_request_method.uri.assert_called_once_with(
        **params
    )


def test_paginated_request_request_method_with_params(
    authenticated_scurri_api,
    paginated_request_subclass_mocked_for_request_method,
    mock_data,
):
    params = {"key": "value"}
    paginated_request_subclass_mocked_for_request_method.request(
        api_session=authenticated_scurri_api, data=mock_data, params=params
    )
    paginated_request_subclass_mocked_for_request_method.uri.assert_called_once_with(
        **params
    )


@pytest.fixture
def mock_carriers_request_response_page_1(carriers_response_data):
    mock_json = MagicMock(return_value=carriers_response_data[0])
    mock_response = MagicMock()
    mock_response.attach_mock(mock_json, "json")
    return mock_response


@pytest.fixture
def mock_carriers_request_response_page_2(carriers_response_data):
    mock_json = MagicMock(return_value=carriers_response_data[1])
    mock_response = MagicMock()
    mock_response.attach_mock(mock_json, "json")
    return mock_response


@pytest.fixture
def mock_paginated_request(
    authenticated_scurri_api,
    mock_paginated_request_subclass,
    mock_carriers_request_response_page_1,
    mock_carriers_request_response_page_2,
):
    mock_request = MagicMock()
    mock_request.side_effect = [
        mock_carriers_request_response_page_1,
        mock_carriers_request_response_page_2,
    ]
    authenticated_scurri_api.session.request = mock_request
    request = mock_paginated_request_subclass()
    return mock_request, request.request(
        api_session=authenticated_scurri_api,
    )


def test_paginated_request_request_method_makes_requests(
    authenticated_scurri_api,
    mock_paginated_request_subclass,
    carriers_response_data,
    mock_paginated_request,
):
    mock_request, response = mock_paginated_request
    calls = [
        call(
            method=GET,
            url=authenticated_scurri_api.base_url
            + mock_paginated_request_subclass.uri(),
            headers=authenticated_scurri_api.get_headers(),
            json=None,
        ),
        call(
            method=GET,
            url=carriers_response_data[0]["next"],
            headers=authenticated_scurri_api.get_headers(),
            json=None,
        ),
    ]
    mock_request.assert_has_calls(calls)


def test_paginated_request_response_returns_paginated_response(
    mock_paginated_request, carriers_response_data
):
    _, response = mock_paginated_request
    expected_response = (
        carriers_response_data[0]["results"] + carriers_response_data[1]["results"]
    )
    assert response == expected_response


def test_carriers_request_uri_method():
    assert CarriersRequest.uri() == "/carriers"


def test_carrier_request_uri_method():
    carrier_slug = "test_carrier"
    assert CarrierRequest.uri(carrier_slug=carrier_slug) == f"/carriers/{carrier_slug}"


def test_carrier_trackings_request_uri_method():
    carrier_slug = "test_carrier"
    assert (
        CarrierTrackingsRequest.uri(carrier_slug=carrier_slug)
        == f"/carriers/{carrier_slug}/trackings"
    )


def test_trackings_request_uri_method():
    assert TrackingsRequest.uri() == "/trackings"


def test_tracking_by_package_id_uri_method():
    package_id = "PACK001"
    assert TrackingByPackageID.uri(package_id=package_id) == f"/trackings/{package_id}"


def test_tracking_by_tracking_number_uri_method():
    carrier_slug = "test_carrier"
    tracking_number = "TRACK0001"
    assert (
        TrackingByTrackingNumber.uri(
            carrier_slug=carrier_slug, tracking_number=tracking_number
        )
        == f"/carriers/{carrier_slug}/trackings/{tracking_number}"
    )
