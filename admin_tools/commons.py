from datetime import datetime

from admin_tools import const
from admin_tools.models import Account


def validate_user(user_id):
    """
    Validates user and returns Account object
    """
    if not (user_id and Account.objects.filter(user_id=user_id).exists()):
        return False, None
    return True, Account.objects.get(user_id=user_id)


def validate_datetime_from_api(datetime_from_api: str):
    """
    Validates and returns datetime object
    """
    try:
        datetime_obj = datetime.strptime(str(datetime_from_api), const.DATE_TIME_FORMAT)
        return True, datetime_obj
    except Exception as exception:
        return False, str(exception)
