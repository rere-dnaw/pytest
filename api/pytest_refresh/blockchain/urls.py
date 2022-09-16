from rest_framework import routers

from blockchain.views import BlockchainViewSet

blockchain_router = routers.DefaultRouter()
blockchain_router.register(
    "blockchain", viewset=BlockchainViewSet, basename="blockchain"
)
