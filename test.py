from scurri import ScurriAPI

USERNAME = "luke@stcstores.co.uk"
PASSWORD = "636Lt$48I$"


def main() -> None:
    api = ScurriAPI(staging=True)
    api.auth(username=USERNAME, password=PASSWORD)
    carriers = api.get_carriers()

    print("get carriers:")
    for carrier in carriers:
        print(carrier.slug)
    print()

    trackings = api.get_carrier_trackings(carrier_slug="hermes")
    print("get carrier trackings:")
    for tracking in trackings:
        print(tracking.id)
    print()

    trackings = api.get_trackings()
    print("get trackings:")
    for tracking in trackings:
        package = tracking
        print(tracking.id)
    print()

    tracking_number = package.tracking_number
    package_carrier = "hermes"
    package_id = package.id

    print("get package by package id")
    package = api.get_tracking_by_package_id(package_id)
    print(package.id)
    print()

    print("get tracking by tracking number")
    package = api.get_tracking_by_tracking_number(
        carrier_slug=package_carrier, tracking_number=tracking_number
    )
    print(package.id)


if __name__ == "__main__":
    main()
