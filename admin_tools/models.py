import random
from django.db import models
from datetime import datetime


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class AccountTypes:
    RIDER = 'rider'
    REQUESTER = 'requester'

    ACCOUNT_TYPES = (
        (RIDER, 'rider'),
        (REQUESTER, 'requester')
    )


class Account(BaseModel):
    """
    An account details for a Rider or Transport Requester
    """
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50)
    account_type = models.CharField(max_length=20, choices=AccountTypes.ACCOUNT_TYPES, null=False)
    # Date/Time when this row was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Date/Time when this row was modified
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.user_id = random.randint(10**7, 10**8-1)
        super(Account, self).save(*args, **kwargs)


class TravelMediums:
    BUS = 'bus'
    CAR = 'car'
    TRAIN = 'train'
    TRAVEL_MEDIUMS = (
        (BUS, 'bus'),
        (CAR, 'car'),
        (TRAIN, 'train')
    )


class RiderTravelStatuses:
    AVAILABLE = 'available'
    NOT_AVAILABLE = 'not_available'
    EXPIRED = 'expired'

    RIDER_TRAVEL_STATUSES = (
        (AVAILABLE, 'available'),
        (NOT_AVAILABLE, 'not_available'),
        (EXPIRED, 'expired')
    )


class RiderTravelInfo(BaseModel):
    """
    Rider Requests (or) Rider Travel information will be stored in this table
    """
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    from_address = models.TextField()
    to_address = models.TextField()
    date_and_time = models.DateTimeField(null=True)
    flexible = models.BooleanField(default=False)
    travel_medium = models.CharField(max_length=20, choices=TravelMediums.TRAVEL_MEDIUMS, null=False)
    asset_quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=RiderTravelStatuses.RIDER_TRAVEL_STATUSES,
                              default=RiderTravelStatuses.AVAILABLE)
    # Date/Time when this row was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Date/Time when this row was modified
    modified_at = models.DateTimeField(auto_now=True)

    @property
    def is_expired(self):
        if self.date_and_time and datetime.now() > self.date_and_time:
            # update the object status
            self.status = RiderTravelStatuses.EXPIRED
            return True
        return False


class AssetTypes:
    LAPTOP = 'laptop'
    TRAVEL_BAG = 'travel_bag'
    PACKAGE = 'package'

    ASSET_TYPES = (
        (LAPTOP, 'laptop'),
        (TRAVEL_BAG, 'travel_bag'),
        (PACKAGE, 'package')
    )


class AssetSensitivities:
    HIGHLY_SENSITIVE = 'highly_sensitive'
    SENSITIVE = 'sensitive'
    NORMAL = 'normal'

    ASSET_SENSITIVITIES = (
        (HIGHLY_SENSITIVE, 'highly_sensitive'),
        (SENSITIVE, 'sensitive'),
        (NORMAL, 'normal')
    )


class TransportRequestStatuses:
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    EXPIRED = 'expired'

    TRANSPORT_REQUEST_STATUSES = (
        (PENDING, 'pending'),
        (CONFIRMED, 'confirmed'),
        (EXPIRED, 'expired')
    )


class TransportationRequests(BaseModel):
    """
    This will have transport requests created by the Requester
    """
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    from_address = models.TextField()
    to_address = models.TextField()
    date_and_time = models.DateTimeField(null=True)
    flexible = models.BooleanField(default=False)
    asset_quantity = models.IntegerField()
    asset_type = models.CharField(max_length=20, choices=AssetTypes.ASSET_TYPES)
    asset_sensitivity = models.CharField(max_length=20, choices=AssetSensitivities.ASSET_SENSITIVITIES)
    # this field to store name and mobile number of the person to whom the package is to be delivered
    whom_to_deliver = models.TextField()
    status = models.CharField(max_length=20, choices=TransportRequestStatuses.TRANSPORT_REQUEST_STATUSES,
                              default=TransportRequestStatuses.PENDING)

    @property
    def is_expired(self):
        if self.date_and_time and datetime.now() > self.date_and_time:
            # update the object status
            self.status = TransportRequestStatuses.EXPIRED
            return True
        return False
