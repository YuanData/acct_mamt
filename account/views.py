from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from .serializers import AccountCreateSerializer, AccountVerifySerializer


class AccountCreateAPIView(APIView):
    def post(self, request):
        serializer = AccountCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        else:
            reason = next(iter(serializer.errors.values()))[0]
            return Response({"success": False, "reason": reason}, status=status.HTTP_400_BAD_REQUEST)


class AccountVerifyAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        failure_key = f"login_failure_{username}"
        failures = cache.get(failure_key, 0)
        if failures >= 5:
            return Response(
                {"success": False, "reason": "Too many failed login attempts. Please try again in 1 minute."},
                status=status.HTTP_429_TOO_MANY_REQUESTS)

        serializer = AccountVerifySerializer(data=request.data)
        if serializer.is_valid():
            cache.set(failure_key, 0, timeout=None)
            return Response({"success": True}, status=status.HTTP_200_OK)
        else:
            cache.set(failure_key, failures + 1, timeout=60)
            reason = next(iter(serializer.errors.values()))[0]
            return Response({"success": False, "reason": reason}, status=status.HTTP_400_BAD_REQUEST)
