from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from classes.models import ClassTimeTable
from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    # we use this serializer to serialize the user model in the browsable api (get its data and display it/allow
    # editing it)
    class Meta:
        model = Account
        fields = ["username", "first_name", "last_name", "email", "avatar", "phone_number"]
        read_only_fields = ["password"]
        # not allowed to edit this attribute, so read only, from tutorial code


# based on the tutorial code
class SignupSerializer(serializers.ModelSerializer):
    # Want a signup form that asks for the user's username, firstname, lastname, email, phone_number
    # and password, we would also like to have an additional field to confirm the password (password2)
    password2 = serializers.CharField(label=_("Confirm password"), write_only=True, style={"input_type": "password"})

    class Meta:
        model = Account  # returns the User model that is active in this project
        fields = ("username", "password", "password2", "first_name", "last_name", "email", "avatar", "phone_number")

        # Specify the input type for password in the sign up, already did for password 2
        # we can also specify the write_only attribute to specify that a field should only be used for writing data
        # and not for reading data
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
        }

    def validate(self, data):  # override validate function to add custom validation
        if data['password'] != data['password2']:  # check if pass matches confirm pass
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data: dict) -> Account:
        # pop password 2
        validated_data.pop('password2')
        # return the created user, use the User create_user method to make the user
        return Account.objects.create_user(**validated_data)
