from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from blockchain.models import Blockchain
from blockchain.serializers import BlockchainSerializer


class BlockchainViewSet(ModelViewSet):
    serializer_class = BlockchainSerializer
    queryset = Blockchain.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination


@api_view(http_method_names=["POST"])
def send_email(request):
    send_mail(
        'Subject here',
        'Here is the message.',
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )
    return Response(
        {"status": "success", "info": "email sent successfully"}, status=200
    )
