from django.urls import path, include
from .views import CreateGameAPIView, SubmitPlayAPIView, GameViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"games", GameViewSet, basename="game")
urlpatterns = [
    path("create-game/", CreateGameAPIView.as_view(), name="create_game"),
    path("submit-play/", SubmitPlayAPIView.as_view(), name="submit_play"),
    path("", include(router.urls)),
]
