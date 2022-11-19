import json
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from requester.utils import RequesterUtils


@method_decorator(csrf_exempt, name="dispatch")
class AddTransportRequest(View):
    """
    View to add transport request from Requester
    """
    def post(self, request):
        user_id = request.GET.get('user_id') or None
        request_body = json.loads(request.body)
        response = RequesterUtils().add_transport_request(user_id=user_id, request_body=request_body)
        return response


@method_decorator(csrf_exempt, name="dispatch")
class GetTransportRequests(View):
    """
    Get Transportation Requests of the Requester
    """
    def post(self, request):
        user_id = request.GET.get('user_id') or None
        try:
            request_body = json.loads(request.body)
        except Exception:
            request_body = None
        response = RequesterUtils.get_transport_requests(user_id=user_id, request_body=request_body)
        return response


@method_decorator(csrf_exempt, name="dispatch")
class RequestRider(View):
    """
    Requester can request the Rider using this API
    """
    def post(self, request):
        request_id = request.GET.get('request_id') or None
        rider_travel_info_id = request.GET.get('rider_travel_info_id') or None
        response = RequesterUtils.request_rider(request_id=request_id, rider_travel_info_id=rider_travel_info_id)
        return response
