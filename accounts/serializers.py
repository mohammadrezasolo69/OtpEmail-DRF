from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import timedelta, datetime

from accounts.ganarate_otp import generate_code_opt
from accounts.models import OTP
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class CustomTokenObtain(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class RequestOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['email']

    def create(self, validated_data):
        email = validated_data.get('email')
        validated_data['code'] = generate_code_opt()
        return super().create(validated_data)


class VerifyOtpSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    new_user = serializers.BooleanField(read_only=True)

    email = serializers.EmailField(required=True)
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        if not OTP.objects.filter(email=email,
                                  code=code,
                                  created_at__gt=datetime.now() - timedelta(minutes=settings.OTP_EXPIRE_TIME)).exists():
            raise serializers.ValidationError('otp code invalid.')
        return data

    # if validate => ok ===> create User

    def create(self, validated_data):
        email = validated_data.get('email')
        user, created = User.objects.get_or_create(email=email, defaults={'email': email, 'is_verify': True})

        if not created:
            if not user.first_name:
                created = True
            if not user.is_verify:
                user.is_verify = True
                user.save()
        validated_data['new_user'] = created

        refresh = CustomTokenObtain.get_token(user)
        access = refresh.access_token
        validated_data['refresh'] = str(refresh)
        validated_data['access'] = str(access)

        return validated_data
