from http import HTTPStatus
from django.http import JsonResponse
from django.forms.models import model_to_dict
from admin_tools.models import AccountTypes, TravelMediums, RiderTravelInfo, RiderTravelStatuses, RequestsMapping, \
    RequestsMappingStatuses
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

        if not user_obj.account_type == AccountTypes.RIDER:
            return JsonResponse({
                'status': 'failure',
                'message': f'only riders can add rider travel info'
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

    @staticmethod
    def check_requests(user_id):
        """
        Check or Get rider requests (requested by Requester)
        """
        # check if user is valid
        status, user_obj = commons.validate_user(user_id=user_id)
        if not status:
            return JsonResponse({
                'status': 'failure',
                'message': f'invalid user id'
            }, status=HTTPStatus.BAD_REQUEST)

        rider_travel_info_obj = RiderTravelInfo.objects.get(user=user_obj, status=RiderTravelStatuses.AVAILABLE)
        if not rider_travel_info_obj:
            return JsonResponse({
                'status': 'failure',
                'message': f'rider travel info is not available'
            }, status=HTTPStatus.BAD_REQUEST)

        requests_mapping_obj = RequestsMapping.objects.filter(travel_info=rider_travel_info_obj,
                                                              status=RequestsMappingStatuses.REQUESTED)

        if not requests_mapping_obj:
            return JsonResponse({
                'status': 'failure',
                'message': 'no requests found for the rider'
            }, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({
            'status': 'success',
            'message': 'data fetched successfully',
            'data': list(requests_mapping_obj.values())
        })

    @staticmethod
    def update_request(request_body):
        """
        Rider can accept or reject the requests he received
        """
        request_id = request_body.get('request_id') or None
        rider_travel_info_id = request_body.get('rider_travel_info_id') or None
        new_status = request_body.get('status') or None

        if not (request_id and rider_travel_info_id and new_status):
            return JsonResponse({
                'status': 'failure',
                'message': 'required details missing!'
            }, status=HTTPStatus.BAD_REQUEST)

        status, request_info_obj = commons.validate_requester_request_id(request_id=request_id)
        if not status:
            return JsonResponse({
                'status': 'failure',
                'message': 'invalid request id'
            }, status=HTTPStatus.BAD_REQUEST)

        status, travel_info_obj = commons.validate_rider_travel_info_id(rider_travel_info_id=rider_travel_info_id)
        if not status:
            return JsonResponse({
                'status': 'failure',
                'message': 'invalid rider travel info id'
            }, status=HTTPStatus.BAD_REQUEST)

        valid_update_statuses = list(dict(RequestsMappingStatuses.REQUEST_MAPPING_STATUSES).keys())
        if new_status not in valid_update_statuses:
            return JsonResponse({
                'status': 'failure',
                'message': 'invalid status received'
            }, status=HTTPStatus.BAD_REQUEST)

        request_mapping_obj = RequestsMapping.objects.filter(travel_info=travel_info_obj,
                                                             request_info=request_info_obj)
        if not request_mapping_obj:
            return JsonResponse({
                'status': 'failure',
                'message': 'no requests found!'
            }, status=HTTPStatus.BAD_REQUEST)

        new_request_mapping_obj = RequestsMapping.objects.filter(
            travel_info=travel_info_obj, request_info=request_info_obj).update(status=new_status)

        # now the rider should be unavailable for new requests
        if new_status in [RequestsMappingStatuses.ACCEPTED]:
            update_travel_info_obj = RiderTravelInfo.objects.filter(
                travel_info_obj=rider_travel_info_id).update(status=RiderTravelStatuses.UNAVAILABLE)

        return JsonResponse({
            'status': 'success',
            'message': 'status updated successfully',
            'data': list(new_request_mapping_obj.values())
        })
