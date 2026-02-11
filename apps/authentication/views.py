from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import LoginSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions_map import ENDPOINT_PERMISSIONS



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            # print(username, password)

            user = authenticate(username=username, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)

                return Response({
                    "token": token.key,
                    "user_id": user.id,
                    "username": user.username
                })

            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PermissionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return all endpoints with granted status for the user
        """
        result = {}
        for endpoint, codename in ENDPOINT_PERMISSIONS.items():
            result[endpoint] = request.user.has_perm(codename)
        return Response(result)