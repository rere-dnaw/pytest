from django.contrib import admin
from blockchain.models import Blockchain


@admin.register(Blockchain)
class BlockchainAdmin(admin.ModelAdmin):
    pass
