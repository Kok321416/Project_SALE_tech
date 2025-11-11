from decimal import Decimal

from django.contrib import admin
from django.db import transaction

from .models import NetworkNode, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    min_num = 0


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ("name", "supplier", "display_level", "city", "country", "debt", "created_at")
    list_filter = ("city",)
    search_fields = ("name", "city", "country", "email")
    ordering = ("name",)
    inlines = (ProductInline,)
    readonly_fields = ("created_at", "display_level")
    list_select_related = ("supplier",)
    actions = ("clear_debt",)

    fieldsets = (
        (None, {"fields": ("name", "supplier", "display_level")}),
        ("Контакты", {"fields": ("email", "country", "city", "street", "house_number")}),
        ("Финансы", {"fields": ("debt",)}),
        ("Системная информация", {"fields": ("created_at",)}),
    )

    @admin.display(description="Уровень")
    def display_level(self, obj: NetworkNode) -> int:
        return obj.level

    @admin.action(description="Очистить задолженность перед поставщиком")
    @transaction.atomic
    def clear_debt(self, request, queryset):
        queryset.update(debt=Decimal("0.00"))


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "node", "release_date")
    list_filter = ("release_date",)
    search_fields = ("name", "model", "node__name")
