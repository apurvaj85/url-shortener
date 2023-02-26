from django.urls import path
from shortener import views

app_name = "shortener"
urlpatterns = [
    path("", views.IndexAPIView.as_view(), name="index"),
    path("shorten_url", views.ShortenURLAPIView.as_view(), name="shorten_url"),
    path(
        "<str:short_url>",
        views.RedirectShortenUrlAPIView.as_view(),
        name="redirect_shorten_url",
    ),
]
