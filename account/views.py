from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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
        serializer = AccountVerifySerializer(data=request.data)
        if serializer.is_valid():
            return Response({"success": True}, status=status.HTTP_200_OK)
        else:
            reason = next(iter(serializer.errors.values()))[0]
            return Response({"success": False, "reason": reason}, status=status.HTTP_400_BAD_REQUEST)
