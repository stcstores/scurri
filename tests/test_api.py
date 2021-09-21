from unittest.mock import Mock, patch

import pytest

from scurri import exceptions, models
from scurri.api import ScurriAPI


@pytest.fixture
def scurri_api():
    return ScurriAPI()


@pytest.fixture
def not_found_response():
    return {"detail": "Not found."}


def test_auth_method(scurri_api, username, password):
    mock_session_auth = Mock()
    scurri_api.session.auth = mock_session_auth
    scurri_api.auth(username=username, password=password)
    mock_session_auth.assert_called_once_with(username=username, password=password)


def test_get_carriers_method(scurri_api, carriers_response_data):
    response_data = (
        carriers_response_data[0]["results"] + carriers_response_data[1]["results"]
    )
    mock_request_method = Mock(return_value=response_data)
    with patch("scurri.api.CarriersRequest.request", mock_request_method):
        response = scurri_api.get_carriers()
    mock_request_method.assert_called_once_with(api_session=scurri_api.session)
    assert len(response) == len(response_data)
    assert isinstance(response[0], models.Carrier)


def test_get_carrier_method(scurri_api, carrier_response_data):
    carrier_slug = "test_carrier"
    mock_request_method = Mock(return_value=carrier_response_data)
    with patch("scurri.api.CarrierRequest.request", mock_request_method):
        response = scurri_api.get_carrier(carrier_slug)
    mock_request_method.assert_called_once_with(
        api_session=scurri_api.session, params={"carrier_slug": carrier_slug}
    )
    assert isinstance(response, models.Carrier)


def test_get_carrier_response_raises_when_carrier_not_found(
    scurri_api, not_found_response
):
    carrier_slug = "test_carrier"
    mock_request_method = Mock(return_value=not_found_response)
    with patch("scurri.api.CarrierRequest.request", mock_request_method):
        with pytest.raises(exceptions.CarrierNotFound):
            scurri_api.get_carrier(carrier_slug)


def test_get_carrier_trackings_method(scurri_api, trackings_response_data):
    mock_request_method = Mock(return_value=trackings_response_data)
    carrier_slug = "test_carrier"
    with patch("scurri.api.CarrierTrackingsRequest.request", mock_request_method):
        response = scurri_api.get_carrier_trackings(carrier_slug)
    mock_request_method.assert_called_once_with(
        api_session=scurri_api.session, params={"carrier_slug": carrier_slug}
    )
    assert len(response) == len(trackings_response_data)
    assert isinstance(response[0], models.TrackedPackage)


def test_get_trackings_method(scurri_api, trackings_response_data):
    mock_request_method = Mock(return_value=trackings_response_data)
    with patch("scurri.api.TrackingsRequest.request", mock_request_method):
        response = scurri_api.get_trackings()
    mock_request_method.assert_called_once_with(api_session=scurri_api.session)
    assert len(response) == len(trackings_response_data)
    assert isinstance(response[0], models.TrackedPackage)


def test_get_trackings_by_package_id_method(scurri_api, tracking_response_data):
    mock_request_method = Mock(return_value=tracking_response_data)
    package_id = "test_package_id"
    with patch("scurri.api.TrackingByPackageID.request", mock_request_method):
        response = scurri_api.get_tracking_by_package_id(package_id)
    mock_request_method.assert_called_once_with(
        api_session=scurri_api.session, params={"package_id": package_id}
    )
    assert isinstance(response, models.TrackedPackage)


def test_get_trackings_by_package_id_raises_when_package_not_found(
    scurri_api, not_found_response
):
    mock_request_method = Mock(return_value=not_found_response)
    package_id = "test_package_id"
    with patch("scurri.api.TrackingByPackageID.request", mock_request_method):
        with pytest.raises(exceptions.PackageNotFound):
            scurri_api.get_tracking_by_package_id(package_id)


def test_get_tracking_by_tracking_number_method(scurri_api, tracking_response_data):
    mock_request_method = Mock(return_value=tracking_response_data)
    carrier_slug = "test_carrier"
    tracking_number = "test_tracking_number"
    with patch("scurri.api.TrackingByTrackingNumber.request", mock_request_method):
        response = scurri_api.get_tracking_by_tracking_number(
            carrier_slug=carrier_slug, tracking_number=tracking_number
        )
    mock_request_method.assert_called_once_with(
        api_session=scurri_api.session,
        params={"carrier_slug": carrier_slug, "tracking_number": tracking_number},
    )
    assert isinstance(response, models.TrackedPackage)


def test_get_tracking_by_tracking_number_raises_when_package_not_found(
    scurri_api, not_found_response
):
    mock_request_method = Mock(return_value=not_found_response)
    carrier_slug = "test_carrier"
    tracking_number = "test_tracking_number"
    with patch("scurri.api.TrackingByTrackingNumber.request", mock_request_method):
        with pytest.raises(exceptions.PackageNotFound):
            scurri_api.get_tracking_by_tracking_number(
                carrier_slug=carrier_slug, tracking_number=tracking_number
            )
