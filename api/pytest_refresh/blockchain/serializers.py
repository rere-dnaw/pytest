from rest_framework import serializers
from .models import Blockchain


class BlockchainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blockchain
        fields = [
            "id",
            "name",
            "ticker",
            "status",
            "last_update",
            "project_url",
            "market_cap",
            "last_price",
            "notes",
        ]
