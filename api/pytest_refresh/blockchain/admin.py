from django.contrib import admin
from .models import Blockchain


@admin.register(Blockchain)
class BlockchainAdmin(admin.ModelAdmin):
    pass
