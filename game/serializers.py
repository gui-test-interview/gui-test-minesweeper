from rest_framework import (
    serializers,
    viewsets,
    response,
    validators,
    decorators,
    status,
)

from .models import Game, Cell


class CellField(serializers.Field):
    """
    Custom serializer for a Cell which hides cell data if a cell is hidden. This is to
    prevent cheating - until a request is made to reveal a cell, no further information
    about that cell is available.
    """

    def to_representation(self, cell: Cell):
        if not cell.visible:
            return {"state": cell.state}
        else:
            return {"count": cell.count, "mine": cell.mine, "state": cell.state}

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            raise validators.ValidationError(
                f"Incorrect type. Expected dict, got {type(data).__name__}"
            )
        return Cell(data)


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"

    id = serializers.CharField(read_only=True)
    date_started = serializers.DateTimeField(read_only=True)
    board = serializers.ListField(
        child=serializers.ListField(child=CellField()), read_only=True
    )
    progress = serializers.FloatField(read_only=True)

    # Exclude the board when getting a list of games.
    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs["child"] = cls()
        kwargs["child"].fields.pop("board")
        return serializers.ListSerializer(*args, **kwargs)

    def create(self, validated_data):
        game = Game(**validated_data)
        game.clean()
        game.save()
        return game


class RevealSerializer(serializers.Serializer):
    row = serializers.IntegerField()
    col = serializers.IntegerField()
    flag = serializers.BooleanField(default=False)


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.order_by("-date_started")
    serializer_class = GameSerializer
    template_name = "index.html"

    # Unset the request in the serializer context to use relavite URLs in the API.
    def get_serializer_context(self):
        return {**super().get_serializer_context(), "request": None}

    # Override rendering due to an issue with template context being passed as a list.
    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == "html":
            return response.Response({})
        return super().list(request, *args, **kwargs)

    @decorators.action(detail=True, methods=["post"])
    def reveal(self, request, pk=None):
        data = RevealSerializer(data=request.data)
        if not data.is_valid():
            return response.Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        row, col = data.validated_data["row"], data.validated_data["col"]
        game = self.get_object()

        if data.validated_data["flag"]:
            game.toggle_flag(row, col)
        else:
            game.reveal(row, col)
        game.save()

        serializer = self.get_serializer(game)
        return response.Response(serializer.data)
