import pytest
from dateutil.parser import isoparse

from scurri import models


@pytest.fixture(scope="module")
def carrier_data():
    return {
        "slug": "colissimo",
        "name": "Colissimo",
        "url": "https://.../api/v1/carriers/colissimo",
        "trackings_url": "https://.../api/v1/carriers/colissimo/trackings",
    }


@pytest.fixture(scope="module")
def tracking_event_data():
    return {
        "id": 2,
        "status": "MANIFESTED",
        "carrier_code": "Some-carrier-code",
        "description": "Some-description",
        "timestamp": "2019-02-11T15:19:06",
        "location": "Location",
    }


@pytest.fixture(scope="module")
def tracking_data(tracking_event_data):
    return {
        "id": 39,
        "tracking_number": "0000000000",
        "url": "https://.../api/v1/carriers/colissimo/trackings/0000000000",
        "created_at": "2019-02-11T15:19:06+00:00",
        "carrier": "Colissimo",
        "carrier_url": "https://.../api/v1/carriers/colissimo",
        "events": [tracking_event_data, tracking_event_data],
    }


@pytest.fixture(scope="module")
def carrier(carrier_data):
    return models.Carrier(carrier_data)


def test_carrier_sets_slug(carrier, carrier_data):
    assert carrier.slug == carrier_data["slug"]


def test_carrier_sets_name(carrier, carrier_data):
    assert carrier.name == carrier_data["name"]


def test_carrier_sets_url(carrier, carrier_data):
    assert carrier.url == carrier_data["url"]


def test_carrier_sets_tracking_url(carrier, carrier_data):
    assert carrier.tracking_url == carrier_data["trackings_url"]


@pytest.fixture(scope="module")
def tracking_event(tracking_event_data):
    return models.TrackingEvent(tracking_event_data)


def test_tracking_event_sets_id(tracking_event, tracking_event_data):
    assert tracking_event.id == tracking_event_data["id"]


def test_tracking_event_sets_status(tracking_event, tracking_event_data):
    assert tracking_event.status == tracking_event_data["status"]


def test_tracking_event_sets_carrier_code(tracking_event, tracking_event_data):
    assert tracking_event.carrier_code == tracking_event_data["carrier_code"]


def test_tracking_event_sets_description(tracking_event, tracking_event_data):
    assert tracking_event.description == tracking_event_data["description"]


def test_tracking_event_sets_timestamp(tracking_event, tracking_event_data):
    assert tracking_event.timestamp == isoparse(tracking_event_data["timestamp"])


def test_tracking_event_sets_location(tracking_event, tracking_event_data):
    assert tracking_event.location == tracking_event_data["location"]


@pytest.fixture(scope="module")
def tracked_package(tracking_data):
    return models.TrackedPackage(tracking_data)


def test_tracked_package_sets_id(tracked_package, tracking_data):
    assert tracked_package.id == tracking_data["id"]


def test_tracked_package_sets_tracking_number(tracked_package, tracking_data):
    assert tracked_package.tracking_number == tracking_data["tracking_number"]


def test_tracked_package_sets_url(tracked_package, tracking_data):
    assert tracked_package.url == tracking_data["url"]


def test_tracked_package_sets_created_at(tracked_package, tracking_data):
    assert tracked_package.created_at == isoparse(tracking_data["created_at"])


def test_tracked_package_sets_carrier(tracked_package, tracking_data):
    assert tracked_package.carrier == tracking_data["carrier"]


def test_tracked_package_sets_carrier_url(tracked_package, tracking_data):
    assert tracked_package.carrier_url == tracking_data["carrier_url"]


def test_tracked_package_sets_events(tracked_package, tracking_data):
    assert type(tracked_package.events) == list
    assert len(tracked_package.events) == 2
    for item in tracked_package.events:
        assert type(item) == models.TrackingEvent
