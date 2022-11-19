from http import HTTPStatus
from django.http import JsonResponse
from django.forms.models import model_to_dict
from admin_tools.models import AssetTypes, AssetSensitivities, TransportationRequests, RequestsMapping, \
    RequestsMappingStatuses
from admin_tools import commons
from requester import const


class RequesterUtils:
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
        asset_quantity = int(request_body.get('asset_quantity')) or None
        asset_type = request_body.get('asset_type') or None
        asset_sensitivity = request_body.get('asset_sensitivity') or None
        whom_to_deliver = request_body.get('whom_to_deliver') or None

        # check if any value is not present
        if not (from_address and to_address and date_and_time and asset_quantity and asset_type
                and asset_sensitivity and whom_to_deliver):
            status, response = False, JsonResponse({
                'status': 'failure',
                'message': 'all the required details are not present'
            }, status=HTTPStatus.BAD_REQUEST)
            return status, response

        valid_asset_types = list(dict(AssetTypes.ASSET_TYPES).keys())
        if asset_type not in valid_asset_types:
            status, response = False, JsonResponse({
                'status': 'failure',
                'message': 'asset type is not valid!'
            }, status=HTTPStatus.BAD_REQUEST)
            return status, response

        valid_asset_sensitivities = list(dict(AssetSensitivities.ASSET_SENSITIVITIES).keys())
        if asset_sensitivity not in valid_asset_sensitivities:
            status, response = False, JsonResponse({
                'status': 'failure',
                'message': 'asset sensitivity is not valid!'
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
            'asset_quantity': request_body.get('asset_quantity'),
            'asset_type': request_body.get('asset_type'),
            'asset_sensitivity': request_body.get('asset_sensitivity'),
            'whom_to_deliver': request_body.get('whom_to_deliver')
        }

    def add_transport_request(self, user_id, request_body):
        """
        Add Requester transport request info to the DB
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
            new_transport_request = TransportationRequests.objects.create(
                user=user_obj,
                from_address=response.get('from_address', ''),
                to_address=response.get('to_address', ''),
                date_and_time=response.get('date_and_time', ''),
                flexible=response.get('flexible', ''),
                asset_quantity=response.get('asset_quantity'),
                asset_type=response.get('asset_type'),
                asset_sensitivity=response.get('asset_sensitivity'),
                whom_to_deliver=response.get('whom_to_deliver')
            )
            response = JsonResponse({
                'status': 'success',
                'message': 'new transport request added',
                'data': model_to_dict(new_transport_request)
            }, status=HTTPStatus.CREATED)
            return response
        except Exception as exception:
            response = JsonResponse({
                'status': 'failure',
                'message': f'adding transport request failed with exception: {exception}'
            }, status=HTTPStatus.BAD_REQUEST)
            return response

    @staticmethod
    def get_transport_requests(user_id, request_body):
        """
        Get Transport Requests requested by the Requester
        """
        # check if user is valid
        status, user_obj = commons.validate_user(user_id=user_id)
        if not status:
            return JsonResponse({
                'status': 'failure',
                'message': f'invalid user id'
            }, status=HTTPStatus.BAD_REQUEST)

        if not request_body:
            # return with all transport requests
            transport_requests_objects = list(TransportationRequests.objects.filter(user=user_obj).values())
            return JsonResponse({
                'status': 'success',
                'message': 'data fetched successfully',
                'data': transport_requests_objects
            })

        filters = request_body.get('filters') or {}
        if not filters:
            # return with all transport requests
            transport_requests_objects = list(TransportationRequests.objects.filter(user=user_obj).values())
            return JsonResponse({
                'status': 'success',
                'message': 'data fetched successfully',
                'data': transport_requests_objects
            })

        valid_filters = {
            key: value for key, value in filters.items() if key in const.VALID_FILTER_KEYS
        }
        # a requester should be able to check only his own requests
        valid_filters['user'] = user_obj

        transport_requests_objects = list(TransportationRequests.objects.filter(**valid_filters).values())
        return JsonResponse({
            'status': 'success',
            'message': 'data fetched successfully',
            'data': transport_requests_objects
        })

    @staticmethod
    def request_rider(request_id, rider_travel_info_id):
        """
        Requester to Request for package
        """
        # check if request id is valid
        status, request_id_obj = commons.validate_requester_request_id(request_id=request_id)
        if not status:
            return JsonResponse({
                'status': 'failure',
                'message': f'invalid request id: {request_id}'
            }, status=HTTPStatus.BAD_REQUEST)

        # check if rider travel info id is valid
        status, rider_travel_info_obj = commons.validate_rider_travel_info_id(
            rider_travel_info_id=rider_travel_info_id)
        if not status:
            return JsonResponse({
                'status': 'failure',
                'message': f'invalid rider travel info id: {rider_travel_info_id}'
            }, status=HTTPStatus.BAD_REQUEST)

        # add request mapping to the DB
        new_rider_request = RequestsMapping.objects.create(
            travel_info=rider_travel_info_obj,
            request_info=request_id_obj,
            status=RequestsMappingStatuses.REQUESTED
        )
        return JsonResponse({
            'status': 'success',
            'message': f'successfully requested the rider',
            'data': model_to_dict(new_rider_request)
        }, status=HTTPStatus.CREATED)
