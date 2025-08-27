from django.urls import path

from .views import health,signup,login,payment_health,create_order, create_service_request,get_user_requests
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path("health/", health),
    path('auth/signup/', signup),
    path('auth/login/', login),
    path('payments/health', payment_health),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('payments/create-order', create_order),

    path('requests', create_service_request),
    path('requests/mine', get_user_requests),

]
