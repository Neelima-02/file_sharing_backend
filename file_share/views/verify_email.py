from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.signing import BadSignature, SignatureExpired
from django.shortcuts import get_object_or_404
from .models import CustomUser


class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            # Unsigned token and validate
            data = signer.unsign_object(token, max_age=3600)  # Link valid for 1 hour
        except SignatureExpired:
            return Response({'error': 'Verification link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except BadSignature:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch user and verify email
        user = get_object_or_404(CustomUser, id=data['user_id'], email=data['email'])
        if user.is_email_verified:
            return Response({'message': 'Email already verified'}, status=status.HTTP_200_OK)

        user.is_email_verified = True
        user.save()

        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
