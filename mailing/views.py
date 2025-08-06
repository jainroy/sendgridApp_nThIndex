from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .serializers import SendMailSerializer, AddEmailSerializer, SendBulkMailSerializer
from .utils import send_basic_email, send_bulk_email
import logging
from .models import Email

logger = logging.getLogger(__name__)

class SendMailView(APIView):
    @swagger_auto_schema(request_body=SendMailSerializer)
    def post(self, request):
        serializer = SendMailSerializer(data=request.data)
        if serializer.is_valid():
            to_mail = serializer.validated_data['to_mail']
            subject = serializer.validated_data['subject']
            content = serializer.validated_data['content']

            try:
                send_basic_email(to_mail, subject, content)
            except Exception as e:
                logger.error(f"SendGrid email sending failed: {str(e)}")
                return Response(
                    {"error": "Failed to send email. Please try again later."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(
                {"message": "Email sent successfully."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AddEmailView(CreateAPIView):
    serializer_class = AddEmailSerializer
    @swagger_auto_schema(request_body=AddEmailSerializer)
    def post(self, request, *args, **kwargs):
        serializer = AddEmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Email added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class SendBulkMailView(APIView):
    @swagger_auto_schema(request_body=SendBulkMailSerializer)
    def post(self, request):
        serializer = SendBulkMailSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data['subject']
            content = serializer.validated_data['content']
            to_mails = list(Email.objects.values_list('email', flat=True))

            try:
                send_bulk_email(to_mails, subject, content)
            except Exception as e:
                logger.error(f"SendGrid bulk email sending failed: {str(e)}")
                return Response(
                    {"error": "Failed to send bulk email."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(
                {"message": "Bulk email sent successfully."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)