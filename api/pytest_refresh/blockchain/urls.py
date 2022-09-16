from rest_framework import routers

from .views import BlockchainViewSet

blockchain_router = routers.DefaultRouter()
blockchain_router.register(
    "blockchain", viewset=BlockchainViewSet, basename="blockchain"
)
