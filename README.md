# Scurri
[![Coverage Status](https://coveralls.io/repos/github/stcstores/scurri/badge.svg?branch=main)](https://coveralls.io/github/stcstores/scurri?branch=main)

Scurri is a python package providing methods for retrieving package tracking information from the [Scurri API](https://www.scurri.com/).

For information about the API see https://scurri.docs.apiary.io/

## Installation

The Scurri package can be installed from github using Pip:

`pip install git+https://github.com/stcstores/scurri.git@main`

## Usage
### Authentication

Methods for accessing the Scurri api are provided by the ScurriAPI class. The `auth` method must be called with your
Scurri username and password to obtain an API Key before any of these methods are called. By default Scurri uses the live
Scurri API. You can select the staging environment instead by passing `staging=True` as a keyword argument to the `auth` method.

If you use any of the API methods without first authenticating `scurri.exceptions.NotAuthorizedException` will be raised.

```python
from scurri import ScurriAPI

scurri_api = ScurriAPI()
scurri_api.auth(username="YOUR_USERNAME", password="YOUR_PASSWORD", staging=False)
```

## API Endpoints

Scurri provides access to the following Scurri API endpoints:
  * List Carriers (/carriers) - Lists available carriers.
  * Carrier Details (/carriers/<carrier-slug>) - Get details of a specific carrier.
  * All Tracking Events (/trackings) - List all current packages and tracking events.
  * All Tracking Events for a Specific Carrier (/carriers/<carrier-slug>/trackings).
  * Events for One Parcel by ID (/trackings/<package-id>).
  * Events for One Parcel by Tracking Number (/carriers/<carrier-slug>/trackings/<tracking-no>).
  
## API Methods

#### List Carriers
 
Retrieve a list of available carriers.

```python
>>> scurri_api.get_carriers()
[<scurri.models.Carrier object at 0x7fcf32e28220>, <scurri.models.Carrier object at 0x7fcf32e283d0>]
```


#### Carrier Details

Return details for a specific carrier. If no carrier is found `scurri.exceptions.CarrierNotFound`
will be raised.

```python
>>> scurri_api.get_carrier('carrier_slug')
<scurri.models.Carrier object at 0x7fcf32e28220>
```


#### All Tracking Events

Return package details and tracking events for all current packages.

```python
>>> scurri_api.get_trackings()
[<scurri.models.TrackedPackage object at 0x7fcf30c4d4f0>, <scurri.models.TrackedPackage object at 0x7fcf30c4d550>]
```

#### All Tracking Events for a Specific Carrier

Return all current tracking events for a given carrier. Will raise `scurri.exceptions.InvalidResponse` if
no matching carrier is found.

```python
>>> scuri_api.get_carrier_trackings('carrier_slug')
[<scurri.models.TrackedPackage object at 0x7fcf30c4d4f0>, <scurri.models.TrackedPackage object at 0x7fcf30c4d550>]
```

#### Events for One Parcel by ID

Return package and tracking event details for a specific package by parcel ID.
If the package is not found `scurri.exceptions.PackageNotFound` will be raised.

```python
>>> scurri_api.get_tracking_by_package_id('package_id')
<scurri.models.TrackedPackage object at 0x7fcf30c4d4f0>
```

#### Events for One Parcel by Tracking Number

Return package and tracking event details for a specific package by tracking number.
If the package is not found `scurri.exceptions.PackageNotFound` will be raised.

```python
>>> scurri_api.get_tracking_by_tracking_number(carrier_slug='carrier_slug', tracking_number='tracking_number')
<scurri.models.TrackedPackage object at 0x7fcf30c4d4f0>
```

## Returned objects

Each API method returns an object, or list of objects, containing the response information from the Scurri API.

#### Carrier - `scurri.models.Carrier`

Attributes:
  * slug: The identification slug for the carrier.
  * name: The name of the carrier.
  * url: The Scurri API endpoint URL used to request information about the carrier.
  * tracking_url: The Scurri API endpoint URL used to request tracked packages for the carrier.
  
#### TrackedPackage - `scurri.models.TrackedPackage`
 
Attributes:
  * id: The ID of the package.
  * tracking_number: The tracking number for the package.
  * url: The Scurri API endpoint URL used to request information about the package.
  * created_at: The date and time the package was added to Scurri (`datetime.datetime`).
  * carrier: The name of the carrier handling the package.
  * carrier_url: The Scurri API endpoint URL used to request current tracking information for
    the package's carrier.
  * carrier_slug: The identification slug for the package's carrier.
  * events: A list of tracking events associated with the package (`list(scurri.models.TrackingEvent)`).
  
#### Tracking Event - `scurri.models.TrackingEvent`

Attributes:
  * id: The ID of the tracking event.
  * status: The status of the package.
  * carrier_code: Unified Scurri status for this event.
  * description: Carrier provided description for this event.
  * timestamp: The date and time of the event (`datetime.datetime`)
  * location: The location related to the event.
  
Statuses:
  * "UNKNOWN" - Carrier's status is not mapped to any of the Scurri statuses
  * "MANIFESTED" - Shipment has been manifested
  * "IN_TRANSIT" - Shipment is in transit
  * "OUT_FOR_DELIVERY" - Shipment out for delivery
  * "DELIVERED" - Shipment delivered
  * "ATTEMPTED_DELIVERY" - An effort was made to deliver the shipment, but the delivery was unsuccessful
  * "EXCEPTION" - Some exception happened during the delivery process

 
