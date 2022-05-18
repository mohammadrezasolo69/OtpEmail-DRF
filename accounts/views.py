from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from accounts.models import OTP
from accounts.serializers import RequestOtpSerializer, VerifyOtpSerializer


class OtpViewSet(viewsets.ModelViewSet):
    queryset = OTP.objects.all()
    serializer_class = RequestOtpSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return RequestOtpSerializer
        return VerifyOtpSerializer

    @action(detail=False, methods=['POST'], url_path='verify')
    def verify_otp(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)