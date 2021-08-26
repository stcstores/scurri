import pytest

import scurri


@pytest.fixture
def username():
    return "mock_user@mock_location.com"


@pytest.fixture
def password():
    return "mock_password1"


@pytest.fixture
def token():
    return "AAA__MOCK_TOKEN_BBB"


@pytest.fixture
def authenticated_scurri_api(requests_mock, token):
    scurri_api = scurri.ScurriAPISession()
    scurri_api.token = token
    return scurri_api


@pytest.fixture
def carriers_response_data():
    response_1 = {
        "count": 7,
        "next": "https://tracking-staging.scurry.co.uk/api/v1/carriers?page=2",
        "previous": None,
        "results": [
            {
                "slug": "dummy_carrier",
                "name": "Dummy Carrier",
                "url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/dummy_carrier",
                "trackings_url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/dummy_carrier/trackings",
            },
            {
                "slug": "collectplus",
                "name": "Collect+",
                "url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/collectplus",
                "trackings_url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/collectplus/trackings",
            },
            {
                "slug": "dpd",
                "name": "DPD",
                "url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/dpd",
                "trackings_url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/dpd/trackings",
            },
            {
                "slug": "ukmail",
                "name": "UKMail",
                "url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/ukmail",
                "trackings_url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/ukmail/trackings",
            },
            {
                "slug": "wndirect",
                "name": "WNDirect",
                "url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/wndirect",
                "trackings_url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/wndirect/trackings",
            },
            {
                "slug": "an-post",
                "name": "AnPost",
                "url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/an-post",
                "trackings_url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/an-post/trackings",
            },
            {
                "slug": "parcelforce",
                "name": "Parcelforce",
                "url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/parcelforce",
                "trackings_url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/parcelforce/trackings",
            },
        ],
    }
    response_2 = {
        "count": 8,
        "next": None,
        "previous": "https://tracking-staging.scurry.co.uk/api/v1/carriers?page=1",
        "results": [
            {
                "slug": "generic-carrier",
                "name": "Generic Carrier",
                "url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/generic-carrier",
                "trackings_url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/generic-carrier/trackings",
            },
            {
                "slug": "yodel",
                "name": "Yodel",
                "url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/yodel",
                "trackings_url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/yodel/trackings",
            },
            {
                "slug": "dhl",
                "name": "DHL",
                "url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/dhl",
                "trackings_url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/dhl/trackings",
            },
            {
                "slug": "hermes",
                "name": "Hermes",
                "url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/hermes",
                "trackings_url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/hermes/trackings",
            },
            {
                "slug": "fastway",
                "name": "Fastway",
                "url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/fastway",
                "trackings_url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/fastway/trackings",
            },
            {
                "slug": "dpd-ireland",
                "name": "DPD Ireland",
                "url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/dpd-ireland",
                "trackings_url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/dpd-ireland/trackings",
            },
            {
                "slug": "on-the-dot",
                "name": "OnTheDot",
                "url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/on-the-dot",
                "trackings_url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/on-the-dot/trackings",
            },
            {
                "slug": "p2p-trakpak",
                "name": "P2P Trakpak",
                "url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/p2p-trakpak",
                "trackings_url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/p2p-trakpak/trackings",
            },
        ],
    }
    return [response_1, response_2]


@pytest.fixture
def carrier_response_data(carriers_response_data):
    return carriers_response_data[0]["results"][0]


@pytest.fixture
def trackings_response_data():
    return [
        {
            "id": 443018,
            "tracking_number": "9669689010150297",
            "url": "https://tracking-staging.scurri.co.uk/api/v1/trackings/443018",
            "created_at": "2021-07-30T10:25:47+00:00",
            "carrier": "Hermes",
            "carrier_url": "https://tracking-staging.scurri.co.uk/api/v1/carriers/hermes",
            "events": [
                {
                    "id": 22206,
                    "status": "IN_TRANSIT",
                    "carrier_code": "kk",
                    "description": "in transit",
                    "timestamp": "2021-07-30T10:35:27",
                    "location": "On van",
                }
            ],
        }
    ]


@pytest.fixture
def tracking_response_data(trackings_response_data):
    return trackings_response_data[0]
