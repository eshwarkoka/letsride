import random
from http import HTTPStatus
from django.http import JsonResponse
from django.forms.models import model_to_dict
from admin_tools.models import Account, AccountTypes


class AccountUtils:
    def __init__(self):
        pass

    @staticmethod
    def generate_user_id():
        """
        Generate unique 8 digit user id which is already not in the DB
        """
        exists_in_db = True
        unique_id = None
        while exists_in_db:
            unique_id = random.randint(10**7, 10**8-1)
            if not Account.objects.filter(user_id=unique_id):
                exists_in_db = False
        return unique_id

    @staticmethod
    def create_account(request_body):
        """
        Util to create the account in DB
        """
        user_name = request_body.get('user_name') or None
        user_email = request_body.get('user_email') or None
        account_type = request_body.get('account_type') or None

        if not (user_name and user_email and account_type):
            response = JsonResponse({
                'status': 'failure',
                'message': 'user name or user email or account_type is empty'
            }, status=HTTPStatus.BAD_REQUEST)
            return response

        valid_account_types = list(dict(AccountTypes.ACCOUNT_TYPES).keys())
        if account_type not in valid_account_types:
            response = JsonResponse({
                'status': 'failure',
                'message': 'account type provided is not valid'
            }, status=HTTPStatus.BAD_REQUEST)
            return response

        try:
            new_account = Account.objects.create(
                user_name=user_name,
                user_email=user_email,
                account_type=account_type
            )
            response = JsonResponse({
                'status': 'success',
                'message': f'account created successfully with user_id: {new_account.user_id}',
                'data': model_to_dict(new_account)
            }, status=HTTPStatus.CREATED)
            return response
        except Exception as exception:
            response = JsonResponse({
                'status': 'failure',
                'message': f'account creation failed with exception: {exception}'
            }, status=HTTPStatus.BAD_REQUEST)
            return response

    @staticmethod
    def delete_account(user_ids: list):
        """
        Util to delete the account(s) in DB
        """
        deleted_user_ids = []
        for user_id in user_ids:
            if Account.objects.filter(user_id=user_id).exists():
                Account.objects.filter(user_id=user_id).delete()
                deleted_user_ids.append(user_id)
        response = JsonResponse({
            'status': 'success',
            'message': f'deleted user ids: {deleted_user_ids}'
        }, status=HTTPStatus.OK)
        return response
