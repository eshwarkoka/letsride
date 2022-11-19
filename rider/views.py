import json
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rider.utils import RiderUtils


@method_decorator(csrf_exempt, name="dispatch")
class AddRiderTravelInfo(View):
    """
    View to add rider info details
    """
    def post(self, request):
        user_id = request.GET.get('user_id') or None
        request_body = json.loads(request.body)
        response = RiderUtils().add_rider_travel_info(user_id=user_id, request_body=request_body)
        return response


@method_decorator(csrf_exempt, name="dispatch")
class GetRiderTravelInfo(View):
    """
    View to add rider info details
    """
    def post(self, request):
        try:
            request_body = json.loads(request.body)
        except Exception:
            request_body = None
        response = RiderUtils.get_rider_travel_info(request_body=request_body)
        return response


@method_decorator(csrf_exempt, name="dispatch")
class CheckRequests(View):
    """
    Rider can check the requests he received from the Receiver
    """
    def get(self, request):
        # use get api to check the requests
        user_id = request.GET.get('user_id') or None
        response = RiderUtils.check_requests(user_id=user_id)
        return response


@method_decorator(csrf_exempt, name="dispatch")
class UpdateRequest(View):
    """
    Rider can update (accept/reject) the requests he received from the Receiver
    """
    def post(self, request):
        request_body = json.loads(request.body)
        response = RiderUtils.update_request(request_body=request_body)
        return response
