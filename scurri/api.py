"""The ScurriAPI class provides methods for interacting with the Scurri API."""

from typing import List

from .apisession import ScurriAPISession
from .models import Carrier, TrackedPackage
from .request import (
    CarrierRequest,
    CarriersRequest,
    CarrierTrackingsRequest,
    TrackingByPackageID,
    TrackingByTrackingNumber,
    TrackingsRequest,
)


class ScurriAPI:
    """The ScurriAPI class provides methods for interacting with the Scurri API."""

    def __init__(self, staging: bool = False) -> None:
        """Create a Scurri API session.

        Call the auth method with you login credentials before making any requests.

        Kwargs:
            staging (bool): If True the Scurri staging API will be used, if False the
                live API will be used. Default False.
        """
        self.session: ScurriAPISession = ScurriAPISession(staging=staging)

    def auth(self, username: str, password: str) -> None:
        """Authorise a Scurri API session.

        Kwargs:
            username (str): Your Scurri account username.
            password (str): Your Scurri account password.
        """
        self.session.auth(username=username, password=password)

    def get_carriers(self) -> List[Carrier]:
        """Return carrier information for all carriers.

        Returns:
            list(scurri.models.Carrier)
        """
        results = CarriersRequest.request(api_session=self.session)
        return [Carrier(result) for result in results]

    def get_carrier(self, carrier_slug: str) -> Carrier:
        """Return carrier information for a given carrier.

        Kwargs:
            carrier_slug (str): The slug name of the carrier to be requested. This can
                be found by requesting a list of couriers with
                scurri.ScurriAPI.get_carriers()

        Returns:
            scurri.models.CarrierRequest
        """
        response = CarrierRequest.request(
            api_session=self.session, params={"carrier_slug": carrier_slug}
        )
        return Carrier(response)

    def get_carrier_trackings(self, carrier_slug: str) -> List[TrackedPackage]:
        """Return tracking information for all packages from a given carrier.

        Kwargs:
            carrier_slug (str): The slug name of the carrier to be requested. This can
                be found by requesting a list of couriers with
                scurri.ScurriAPI.get_carriers()

        Returns:
            list(scurri.models.TrackedPackage)
        """
        results = CarrierTrackingsRequest.request(
            params={"carrier_slug": carrier_slug}, api_session=self.session
        )
        return [TrackedPackage(result) for result in results]

    def get_trackings(self) -> List[TrackedPackage]:
        """Return tracking information for all packages.

        Returns:
            list(scurri.models.TrackedPackage)
        """
        results = TrackingsRequest.request(api_session=self.session)
        return [TrackedPackage(result) for result in results]

    def get_tracking_by_package_id(self, package_id: str) -> TrackedPackage:
        """Return tracking information for a package by package ID.

        Kwargs:
            package_id (str): The ID of the package to be requested.

        Returns:
            scurri.models.TrackedPackage
        """
        response = TrackingByPackageID.request(
            api_session=self.session, params={"package_id": package_id}
        )
        return TrackedPackage(response)

    def get_tracking_by_tracking_number(
        self, carrier_slug: str, tracking_number: str
    ) -> TrackedPackage:
        """Return tracking information for a package by tracking number.

        Kwargs:
            carrier_slug (str): The slug name of the carrier to be requested. This can
                be found by requesting a list of couriers with
                scurri.ScurriAPI.get_carriers()

            tracking_number (str): The tracking number of the package to be requested.

        Returns:
            scurri.models.TrackedPackage
        """
        response = TrackingByTrackingNumber.request(
            api_session=self.session,
            params={"carrier_slug": carrier_slug, "tracking_number": tracking_number},
        )
        return TrackedPackage(response)
