from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.models import Account
from accounts.serializers import AccountSerializer, SignupSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class SignUpView(APIView):
    """
    Allows a user to register on the website.
    """
    # reference: https://thinkster.io/tutorials/django-json-api/authentication
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    @swagger_auto_schema(request_body=SignupSerializer)
    def post(self, request):
        sign_up_serializer = self.serializer_class(data=request.data)
        sign_up_serializer.is_valid(raise_exception=True)
        sign_up_serializer.save()

        return Response(sign_up_serializer.data, status=status.HTTP_201_CREATED)


class AccountView(RetrieveAPIView):
    """
    View a given account.
    """
    serializer_class = AccountSerializer

    def get_object(self):
        return get_object_or_404(Account, id=self.kwargs['account_id'])


class AccountUpdateView(UpdateAPIView):
    """
    Allows a user to update their account details.
    """
    permission_classes = [IsAuthenticated]
    # make sure user is logged in
    serializer_class = AccountSerializer

    def get_object(self):
        return get_object_or_404(Account, id=self.request.user.pk)
        # use request.user.pk so that the logged in user can only edit their own profile
