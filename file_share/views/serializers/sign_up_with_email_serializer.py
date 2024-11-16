from rest_framework import serializers


class SignUpWithEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)

    class Meta:
        fields = ['email', 'password']
