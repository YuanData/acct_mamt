from django.core.cache import cache
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AccountCreateSerializer, AccountVerifySerializer


class AccountCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='Create Account',
        operation_description='Password need containing at least 1 uppercase letter, 1 lowercase letter, and 1 number',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, minLength=3, maxLength=32),
                'password': openapi.Schema(type=openapi.TYPE_STRING, minLength=8, maxLength=32)},
            required=['username', 'password']),
        responses={
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'success': openapi.Schema(type=openapi.TYPE_BOOLEAN)},
                required=['success']
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'reason': openapi.Schema(type=openapi.TYPE_STRING)},
                required=['success', 'reason'])})
    def post(self, request):
        serializer = AccountCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        else:
            reason = next(iter(serializer.errors.values()))[0]
            return Response({"success": False, "reason": reason}, status=status.HTTP_400_BAD_REQUEST)


class AccountVerifyAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='Verify Account and Password',
        operation_description='If the password verification fails 5 times, the user should wait 1 minute before attempting to verify the password again',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, minLength=3, maxLength=32, ),
                'password': openapi.Schema(type=openapi.TYPE_STRING, minLength=8, maxLength=32)},
            required=['username', 'password']),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'success': openapi.Schema(type=openapi.TYPE_BOOLEAN)},
                required=['success']
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'reason': openapi.Schema(type=openapi.TYPE_STRING)},
                required=['success', 'reason']), })
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
