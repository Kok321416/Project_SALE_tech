from collections import Counter

from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView
from rest_framework import viewsets

from .filters import NetworkNodeFilter
from .models import NetworkNode, Product
from .permissions import IsActiveStaff
from .serializers import NetworkNodeSerializer


class HomePageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        nodes = (
            NetworkNode.objects.select_related("supplier")
            .prefetch_related("products")
            .all()
        )

        total_nodes = nodes.count()
        total_products = Product.objects.count()
        countries_count = nodes.values("country").distinct().count()

        level_counter = Counter()
        for node in nodes:
            level_counter[node.level] += 1

        level_cards = [
            {
                "title": "Заводы",
                "description": "Производители оборудования, формируют уровень 0 цепочки.",
                "count": level_counter.get(0, 0),
            },
            {
                "title": "Розничные сети",
                "description": "Оптовые покупатели и региональные сети, напрямую или опосредованно связанные с заводами.",
                "count": level_counter.get(1, 0),
            },
            {
                "title": "Индивидуальные предприниматели",
                "description": "Финальное звено поставок, обслуживающее конечных покупателей.",
                "count": level_counter.get(2, 0),
            },
        ]

        featured_nodes = (
            nodes.order_by("-created_at")[:3]
            if total_nodes
            else []
        )

        context.update(
            {
                "admin_url": reverse("admin:index"),
                "api_url": reverse("network-node-list"),
                "stats_cards": [
                    {
                        "title": "Звенья сети",
                        "value": total_nodes,
                        "description": "Все участники цепочки поставок",
                    },
                    {
                        "title": "Каталог продуктов",
                        "value": total_products,
                        "description": "Актуальные устройства и модели",
                    },
                    {
                        "title": "Страны присутствия",
                        "value": countries_count,
                        "description": "География сети продаж",
                    },
                ],
                "level_cards": level_cards,
                "featured_nodes": featured_nodes,
                "has_network": total_nodes > 0,
            }
        )
        return context


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
