from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import exceptions, serializers
from .models import CustomUser


class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid email or password")

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Invalid email or password")

        access_token = AccessToken.for_user(user)
        return {"access_token": str(access_token)}


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        access_token = AccessToken.for_user(user)
        return {"access_token": str(access_token)}


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email")
