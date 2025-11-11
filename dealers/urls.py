from django.urls import path

from .views import NetworkNodeDetailView, NetworkNodeListView

app_name = "dealers"

urlpatterns = [
    path("", NetworkNodeListView.as_view(), name="node-list"),
    path("<int:pk>/", NetworkNodeDetailView.as_view(), name="node-detail"),
]

