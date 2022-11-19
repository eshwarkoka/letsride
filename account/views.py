import ast
import json
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from account.utils import AccountUtils


@method_decorator(csrf_exempt, name="dispatch")
class CreateAccount(View):
    """
    API to create account of Rider or Requester in DB
    """
    def post(self, request):
        request_body = json.loads(request.body)
        response = AccountUtils().create_account(request_body=request_body)
        return response


@method_decorator(csrf_exempt, name="dispatch")
class DeleteAccount(View):
    """
    API to delete an account
    """
    def post(self, request):
        user_ids = request.GET.get('user_ids')
        # convert str of list to list of user ids
        user_ids = ast.literal_eval(user_ids)
        response = AccountUtils().delete_account(user_ids=user_ids)
        return response
