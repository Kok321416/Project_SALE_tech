from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class NetworkNode(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    street = models.CharField(max_length=128)
    house_number = models.CharField(max_length=32)
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="clients",
        null=True,
        blank=True,
    )
    debt = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"

    def __str__(self) -> str:
        return f"{self.name} ({self.city}, {self.country})"

    def clean(self) -> None:
        if self.supplier_id and self.supplier_id == self.pk:
            raise ValidationError("Звено сети не может быть своим собственным поставщиком.")

        supplier = self.supplier
        seen_suppliers = set()
        depth = 0

        while supplier:
            if supplier.pk in seen_suppliers:
                raise ValidationError("Обнаружен цикл поставщиков. Проверьте выбранного поставщика.")
            seen_suppliers.add(supplier.pk)
            depth += 1
            if depth > 2:
                raise ValidationError("Глубина иерархии не может превышать трех уровней.")
            supplier = supplier.supplier

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def level(self) -> int:
        supplier = self.supplier
        depth = 0
        while supplier:
            depth += 1
            supplier = supplier.supplier
        return depth


class Product(models.Model):
    node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Звено сети",
    )
    name = models.CharField(max_length=255, verbose_name="Название")
    model = models.CharField(max_length=255, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата выхода на рынок")

    class Meta:
        ordering = ("name", "model")
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self) -> str:
        return f"{self.name} {self.model}"
