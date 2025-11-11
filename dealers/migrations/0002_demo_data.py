from django.db import migrations
def create_demo_nodes(apps, schema_editor):
    NetworkNode = apps.get_model("dealers", "NetworkNode")
    Product = apps.get_model("dealers", "Product")

    factory = NetworkNode.objects.create(
        name="Aurora Electronics Factory",
        email="factory@aurora.example",
        country="Germany",
        city="Berlin",
        street="Innovationsallee",
        house_number="12A",
        debt="0.00",
    )

    retail = NetworkNode.objects.create(
        name="ElectroLine Retail",
        email="info@electroline.example",
        country="Germany",
        city="Hamburg",
        street="Commerceplatz",
        house_number="7",
        supplier=factory,
        debt="8250.30",
    )

    entrepreneur = NetworkNode.objects.create(
        name="TechPoint Entrepreneur",
        email="contact@techpoint.example",
        country="France",
        city="Paris",
        street="Rue de Startups",
        house_number="42",
        supplier=retail,
        debt="1450.00",
    )

    Product.objects.bulk_create(
        [
            Product(
                node=factory,
                name="Aurora Vision TV",
                model="AV-55Q9",
                release_date="2024-03-15",
            ),
            Product(
                node=factory,
                name="Aurora Sound Speaker",
                model="AS-360",
                release_date="2023-11-02",
            ),
            Product(
                node=retail,
                name="Smart Home Hub",
                model="SH-200",
                release_date="2024-05-20",
            ),
            Product(
                node=entrepreneur,
                name="Energy Saver Adapter",
                model="ES-15",
                release_date="2024-01-10",
            ),
        ]
    )


def remove_demo_nodes(apps, schema_editor):
    NetworkNode = apps.get_model("dealers", "NetworkNode")
    NetworkNode.objects.filter(
        name__in=[
            "Aurora Electronics Factory",
            "ElectroLine Retail",
            "TechPoint Entrepreneur",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("dealers", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_demo_nodes, remove_demo_nodes, elidable=True),
    ]

