from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    The serializer for registering a new user.
    """

    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        min_length=8, write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ("username", "password", "email")
        extra_kwargs = {"username": {"min_length": 3}}

    def create(self, validated_data):
        """
        Creates a new user with the given data.
        """
        user = User.objects.create_user(**validated_data)

        return user
