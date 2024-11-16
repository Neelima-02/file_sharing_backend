from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from file_share.views.serializers.sign_up_with_email_serializer import \
    SignUpWithEmailSerializer
from file_share.models import UserAccount
from django.contrib.auth.password_validation import validate_password
from django.core.signing import Signer, TimestampSigner
from file_share.models import UserRoleEnum
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="post")
class SignUpWithEmailView(APIView):

    def post(self, request):
        serializer = SignUpWithEmailSerializer(data=request.data)
        if serializer.is_valid():
            request_data = serializer.data

            try:
                validate_password(request_data["password"])
            except ValidationError:
                return Response({
                    'error': 'Password is too weak'
                }, status=status.HTTP_400_BAD_REQUEST)

            email = request_data["email"]
            if UserAccount.objects.filter(email=email).exists():
                return Response({
                    'error': 'Email already exists'
                }, status=status.HTTP_400_BAD_REQUEST)

            user = UserAccount.objects.create(
                email=email,
                password=request_data["password"],
                role=UserRoleEnum.CLIENT.value)

            self._send_verification_email(user)

            return Response({
                'message': 'User account created successfully. Please verify your email.',
                'user_id': str(user.user_id)
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def _send_verification_email(user):
        signer = TimestampSigner()

        email_verification_token = signer.sign_object(
            {'user_id': str(user.user_id), 'email': user.email})
        verification_link = f"{settings.SITE_URL}/api/file-share/user/verify-email/v1/{email_verification_token}"

        send_mail(
            subject="Verify Your Email Address",
            message=f"Please click the link below to verify your email:\n{verification_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
