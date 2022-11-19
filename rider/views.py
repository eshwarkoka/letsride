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
        request_body = json.loads(request.body)
        response = RiderUtils().add_rider_travel_info(request_body=request_body)
        return response


@method_decorator(csrf_exempt, name="dispatch")
class GetRiderTravelInfo(View):
    """
    View to add rider info details
    """
    def post(self, request):
        request_body = json.loads(request.body)
        response = RiderUtils().get_rider_travel_info(request_body=request_body)
        return response
