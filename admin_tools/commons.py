from datetime import datetime

from admin_tools import const
from admin_tools.models import Account, TransportationRequests, RiderTravelInfo


def validate_user(user_id):
    """
    Validates user and returns Account object
    """
    if not (user_id and Account.objects.filter(user_id=user_id).exists()):
        return False, None
    return True, Account.objects.get(user_id=user_id)


def validate_requester_request_id(request_id):
    """
    Validates Requester's request id and returns TransportationRequests object
    """
    if not (request_id and TransportationRequests.objects.filter(request_id=request_id).exists()):
        return False, None
    return True, TransportationRequests.objects.get(request_id=request_id)


def validate_rider_travel_info_id(rider_travel_info_id):
    """
    Validates Rider's travel info id and returns RiderTravelInfo object
    """
    if not (rider_travel_info_id and RiderTravelInfo.objects.filter(
            travel_info_id=rider_travel_info_id).exists()):
        return False, None
    return True, RiderTravelInfo.objects.get(travel_info_id=rider_travel_info_id)


def validate_datetime_from_api(datetime_from_api: str):
    """
    Validates and returns datetime object
    """
    try:
        datetime_obj = datetime.strptime(str(datetime_from_api), const.DATE_TIME_FORMAT)
        return True, datetime_obj
    except Exception as exception:
        return False, str(exception)
