from django.urls import path
from file_share.views.sign_up_with_email import SignUpWithEmailView
from file_share.views.verify_email_view import VerifyEmailView


urlpatterns = [
    path('user/sign-up/v1/', SignUpWithEmailView.as_view(),
         name='signup-with-email'),
    path('user/verify-email/v1/<str:token>/', VerifyEmailView.as_view(),
         name='verify-email')
]
