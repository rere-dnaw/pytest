from rest_framework import serializers
from blockchain.models import Blockchain


class BlockchainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blockchain
        fields = [
            "id",
            "name",
            "ticker",
            "type",
            "last_update",
            "project_url",
            "market_cap",
            "last_price",
            "notes",
        ]
