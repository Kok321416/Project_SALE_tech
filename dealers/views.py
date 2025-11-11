from django.views.generic import DetailView, ListView
from rest_framework import viewsets

from .filters import NetworkNodeFilter
from .models import NetworkNode
from .permissions import IsActiveStaff
from .serializers import NetworkNodeSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = (
        NetworkNode.objects.select_related("supplier")
        .prefetch_related("products")
        .all()
    )
    serializer_class = NetworkNodeSerializer
    permission_classes = (IsActiveStaff,)
    filterset_class = NetworkNodeFilter
    search_fields = ("name", "city", "country", "email")
    ordering_fields = ("name", "city", "country", "created_at", "debt")


class NetworkNodeListView(ListView):
    template_name = "dealers/node_list.html"
    context_object_name = "nodes"

    def get_queryset(self):
        return (
            NetworkNode.objects.select_related("supplier")
            .prefetch_related("products")
            .order_by("name")
        )


class NetworkNodeDetailView(DetailView):
    model = NetworkNode
    template_name = "dealers/node_detail.html"
    context_object_name = "node"

    def get_queryset(self):
        return (
            NetworkNode.objects.select_related("supplier")
            .prefetch_related("products")
            .all()
        )
