"""Models for scurri data."""

from datetime import datetime
from typing import Any, Dict, List

from dateutil.parser import isoparse


class Carrier:
    """Model for carrier data."""

    SLUG = "slug"
    NAME = "name"
    URL = "url"
    TRACKING_URL = "trackings_url"

    def __init__(self, kwargs: Dict[str, Any]) -> None:
        self.slug: str = kwargs[self.SLUG]
        self.name: str = kwargs[self.NAME]
        self.url: str = kwargs[self.URL]
        self.tracking_url: str = kwargs[self.TRACKING_URL]


class TrackingEvent:
    """Model for tracking event data."""

    ID = "id"
    STATUS = "status"
    CARRIER_CODE = "carrier_code"
    DESCRIPTION = "description"
    TIMESTAMP = "timestamp"
    LOCATION = "location"

    def __init__(self, kwargs: Dict[str, Any]) -> None:
        self.id: str = kwargs[self.ID]
        self.status: str = kwargs[self.STATUS]
        self.carrier_code: str = kwargs[self.CARRIER_CODE]
        self.description: str = kwargs[self.DESCRIPTION]
        self.timestamp: datetime = isoparse(kwargs[self.TIMESTAMP])
        self.location: str = kwargs[self.LOCATION]


class TrackedPackage:
    """Model for tracked package data."""

    ID = "id"
    TRACKING_NUMBER = "tracking_number"
    URL = "url"
    CREATED_AT = "created_at"
    CARRIER = "carrier"
    CARRIER_URL = "carrier_url"
    EVENTS = "events"

    def __init__(self, kwargs: Dict[str, Any]) -> None:
        self.id: str = kwargs[self.ID]
        self.tracking_number: str = kwargs[self.TRACKING_NUMBER]
        self.url: str = kwargs[self.URL]
        self.created_at: datetime = isoparse(kwargs[self.CREATED_AT])
        self.carrier: str = kwargs[self.CARRIER]
        self.carrier_url: str = kwargs[self.CARRIER_URL]
        self.events: List[TrackingEvent] = [
            TrackingEvent(event) for event in kwargs[self.EVENTS]
        ]
