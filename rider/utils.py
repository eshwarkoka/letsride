from http import HTTPStatus
from django.http import JsonResponse
from django.forms.models import model_to_dict
from admin_tools.models import TravelMediums, RiderTravelInfo, RiderTravelStatuses
from admin_tools import commons
from rider import const


class RiderUtils:
    def __init__(self):
        pass

    @staticmethod
    def validate_request_body(request_body):
        """
        Validate the request body
        """
        from_address = request_body.get('from_address') or None
        to_address = request_body.get('to_address') or None
        date_and_time = request_body.get('date_and_time') or None
        flexible = request_body.get('from_address') or None
        travel_medium = request_body.get('travel_medium') or None
        asset_quantity = int(request_body.get('asset_quantity')) or None

        # check if any value is not present
        if not (from_address and to_address and date_and_time and travel_medium and asset_quantity):
            status, response = False, JsonResponse({
                'status': 'failure',
                'message': 'all the required details are not present'
            }, status=HTTPStatus.BAD_REQUEST)
            return status, response

        valid_travel_mediums = list(dict(TravelMediums.TRAVEL_MEDIUMS).keys())
        if travel_medium not in valid_travel_mediums:
            status, response = False, JsonResponse({
                'status': 'failure',
                'message': 'travel medium is not valid!'
            }, status=HTTPStatus.BAD_REQUEST)
            return status, response

        status, date_and_time = commons.validate_datetime_from_api(datetime_from_api=date_and_time)
        if not status:
            exception_message = date_and_time
            response = JsonResponse({
                'status': 'failure',
                'message': f'Exception: {exception_message}'
            }, status=HTTPStatus.BAD_REQUEST)
            return status, response

        flexible = True if str(flexible).lower() in ['true'] else False

        return True, {
            'from_address': request_body.get('from_address'),
            'to_address': request_body.get('to_address'),
            'date_and_time': date_and_time,
            'flexible': flexible,
            'travel_medium': request_body.get('travel_medium'),
            'asset_quantity': request_body.get('asset_quantity')
        }

    def add_rider_travel_info(self, user_id, request_body):
        """
        Add Rider travel info to the DB
        """
        # check if user is valid
        status, user_obj = commons.validate_user(user_id=user_id)
        if not status:
            return JsonResponse({
                'status': 'failure',
                'message': f'invalid user id'
            }, status=HTTPStatus.BAD_REQUEST)

        status, response = self.validate_request_body(request_body=request_body)
        if not status:
            return response

        try:
            new_travel_info = RiderTravelInfo.objects.create(
                user=user_obj,
                from_address=response.get('from_address', ''),
                to_address=response.get('to_address', ''),
                date_and_time=response.get('date_and_time', ''),
                flexible=response.get('flexible', ''),
                travel_medium=response.get('travel_medium'),
                asset_quantity=response.get('asset_quantity')
            )
            response = JsonResponse({
                'status': 'success',
                'message': 'new rider travel info added',
                'data': model_to_dict(new_travel_info)
            }, status=HTTPStatus.CREATED)
            return response
        except Exception as exception:
            response = JsonResponse({
                'status': 'failure',
                'message': f'adding travel info failed with exception: {exception}'
            }, status=HTTPStatus.BAD_REQUEST)
            return response

    @staticmethod
    def get_rider_travel_info(request_body):
        """
        Get Rider travel info from the db
        """
        if not request_body:
            # return with all rider travel info
            travel_info_objects = list(RiderTravelInfo.objects.filter(status=RiderTravelStatuses.AVAILABLE).values())
            return JsonResponse({
                'status': 'success',
                'message': 'data fetched successfully',
                'data': travel_info_objects
            })

        filters = request_body.get('filters') or {}
        if not filters:
            travel_info_objects = list(RiderTravelInfo.objects.filter(status=RiderTravelStatuses.AVAILABLE).values())
            return JsonResponse({
                'status': 'success',
                'message': 'data fetched successfully',
                'data': travel_info_objects
            })

        valid_filters = {
            key: value for key, value in filters.items() if key in const.VALID_FILTER_KEYS
        }
        valid_filters['status'] = RiderTravelStatuses.AVAILABLE

        travel_info_objects = list(RiderTravelInfo.objects.filter(**valid_filters).values())
        return JsonResponse({
            'status': 'success',
            'message': 'data fetched successfully',
            'data': travel_info_objects
        })
