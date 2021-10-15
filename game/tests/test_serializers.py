import uuid
import pytest
from rest_framework.test import APIRequestFactory
from game.models import Game, CellState
from game.serializers import GameViewSet

pytestmark = pytest.mark.django_db


def test_game_list():
    factory = APIRequestFactory()
    request = factory.get("/", format="json", HTTP_ACCEPT="application/json")
    response = GameViewSet.as_view({"get": "list"})(request)

    assert response.data == []

    pk = str(uuid.uuid4())
    game = Game(pk=pk, width=9, height=9, mines=10)
    game.initialize()
    game.save()

    response = GameViewSet.as_view({"get": "list"})(request)

    assert len(response.data) == 1
    assert response.data[0]["id"] == pk
    assert response.data[0]["width"] == 9
    assert response.data[0]["height"] == 9
    assert response.data[0]["mines"] == 10

    # No board data in list endpoint.
    assert "board" not in response.data[0]


def test_game_retrieve():
    pk = str(uuid.uuid4())

    factory = APIRequestFactory()
    request = factory.get("/", format="json", HTTP_ACCEPT="application/json")
    response = GameViewSet.as_view({"get": "retrieve"})(request, pk=pk)

    assert response.status_code == 404

    game = Game(pk=pk, width=9, height=9, mines=10)
    game.initialize()
    game.save()

    response = GameViewSet.as_view({"get": "retrieve"})(request, pk=pk)

    assert response.data["id"] == pk
    assert response.data["width"] == 9
    assert response.data["height"] == 9
    assert response.data["mines"] == 10

    # All cells are hidden by default.
    assert all(
        cell == {"state": CellState.HIDDEN}
        for row in response.data["board"]
        for cell in row
    )
