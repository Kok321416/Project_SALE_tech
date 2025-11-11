"""
URL configuration for sale_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from dealers.views import NetworkNodeViewSet

router = DefaultRouter()
router.register("network-nodes", NetworkNodeViewSet, basename="network-node")

urlpatterns = [
    path(
        "",
        TemplateView.as_view(
            template_name="landing.html",
            extra_context={
                "admin_url": "/admin/",
                "api_url": "/api/network-nodes/",
            },
        ),
        name="home",
    ),
    path("network/", include(("dealers.urls", "dealers"), namespace="dealers")),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path(
        "api/docs/",
        TemplateView.as_view(
            template_name="api_docs.html",
            extra_context={
                "endpoints": [
                    {"method": "GET", "path": "/api/network-nodes/", "description": "Список звеньев сети"},
                    {"method": "POST", "path": "/api/network-nodes/", "description": "Создание звена"},
                    {"method": "GET", "path": "/api/network-nodes/<id>/", "description": "Детали звена"},
                    {"method": "PATCH", "path": "/api/network-nodes/<id>/", "description": "Обновление звена без изменения долга"},
                    {"method": "DELETE", "path": "/api/network-nodes/<id>/", "description": "Удаление звена"},
                    {"method": "GET", "path": "/api/network-nodes/?country=Germany", "description": "Фильтрация по стране"},
                ]
            },
        ),
        name="api-docs",
    ),
    path("api/auth/", include("rest_framework.urls")),
]
