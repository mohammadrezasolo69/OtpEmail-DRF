from django.urls import path, include
from accounts import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('otp', views.OtpViewSet, basename='otp')

app_name = 'accounts'
urlpatterns = [
    path('', include(router.urls))
]
