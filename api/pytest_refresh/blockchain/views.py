from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from blockchain.models import Blockchain
from blockchain.serializers import BlockchainSerializer


class BlockchainViewSet(ModelViewSet):
    serializer_class = BlockchainSerializer
    queryset = Blockchain.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination
