from django.urls import path
from .views import UserGetPostData, RegisterView, UsersUpdateAndDeleteView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'contacts'

urlpatterns = [
    # ----- API endpoints -----
    path('register/', RegisterView.as_view(), name='api-register'),
    path('contacts/', UserGetPostData.as_view(), name='api-contacts'),
    path('contacts/<int:pk>/', UsersUpdateAndDeleteView.as_view(), name='api-contact-detail'),

    # ----- JWT Authentication -----
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
