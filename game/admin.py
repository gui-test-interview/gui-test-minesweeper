from django.contrib import admin
from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "width",
        "height",
        "mines",
        "state",
        "date_started",
        "date_ended",
    )
