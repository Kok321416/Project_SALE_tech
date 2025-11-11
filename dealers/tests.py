from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import NetworkNode


class NetworkNodeAPITestCase(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="staff_user",
            email="staff@example.com",
            password="password123",
            is_staff=True,
            is_active=True,
        )
        self.client.force_authenticate(self.user)

        self.factory = NetworkNode.objects.create(
            name="Main Test Factory",
            email="factory@example.com",
            country="Germany",
            city="Berlin",
            street="Tech Street",
            house_number="1",
            debt="0.00",
        )

    def test_create_network_node(self):
        url = reverse("network-node-list")
        payload = {
            "name": "Retail Chain",
            "email": "retail@example.com",
            "country": "Germany",
            "city": "Hamburg",
            "street": "Commerce Ave",
            "house_number": "10",
            "supplier": self.factory.id,
            "debt": "1500.50",
        }

        response = self.client.post(url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["level"], 1)
        self.assertEqual(response.data["supplier"], self.factory.id)

    def test_update_cannot_change_debt(self):
        node = NetworkNode.objects.create(
            name="Retail Chain",
            email="retail@example.com",
            country="Germany",
            city="Hamburg",
            street="Commerce Ave",
            house_number="10",
            supplier=self.factory,
            debt="1500.50",
        )
        url = reverse("network-node-detail", args=[node.id])

        response = self.client.patch(url, data={"debt": "0.00"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("debt", response.data)

    def test_filter_by_country(self):
        NetworkNode.objects.create(
            name="Entrepreneur One",
            email="entrepreneur1@example.com",
            country="Germany",
            city="Munich",
            street="Startup Str",
            house_number="5A",
            supplier=self.factory,
            debt="200.00",
        )
        NetworkNode.objects.create(
            name="Entrepreneur Two",
            email="entrepreneur2@example.com",
            country="France",
            city="Paris",
            street="Innovation Blvd",
            house_number="42",
            supplier=self.factory,
            debt="350.00",
        )

        url = reverse("network-node-list")
        response = self.client.get(url, data={"country": "Germany"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_names = {node["name"] for node in response.data}
        self.assertIn("Main Test Factory", returned_names)
        self.assertIn("Entrepreneur One", returned_names)
        self.assertNotIn("Entrepreneur Two", returned_names)

    def test_permission_denied_for_non_staff(self):
        user_model = get_user_model()
        regular_user = user_model.objects.create_user(
            username="regular_user",
            email="regular@example.com",
            password="password123",
            is_staff=False,
            is_active=True,
        )
        self.client.force_authenticate(regular_user)

        url = reverse("network-node-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
