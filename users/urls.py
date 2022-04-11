from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import EmailTokenObtainPairView, RegisterView, CarAPIView,\
    ShortenerListAPIView, ShortenerCreateApiView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='token_obtain_pair'),
    path('car/<str:pk>/', CarAPIView.as_view(), name='car'),
    path('list/', ShortenerListAPIView.as_view(), name='all_links'),
    path('create/', ShortenerCreateApiView.as_view(), name='create_api'),
    path('token/obtain/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]