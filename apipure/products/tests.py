import json

from django.test import TestCase
from django.urls import reverse

from .models import Product


class ProductApiTests(TestCase):
    def test_creates_and_lists_a_product(self):
        response = self.client.post(
            reverse("products:product-list"),
            data=json.dumps({"name": "Teclado", "price": "29.99", "stock": 8}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["price"], "29.99")

        response = self.client.get(reverse("products:product-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)

    def test_rejects_invalid_product(self):
        response = self.client.post(
            reverse("products:product-list"),
            data=json.dumps({"name": "", "price": -1, "stock": -1}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("price", response.json()["errors"])

    def test_rejects_a_price_with_more_than_two_decimals(self):
        response = self.client.post(
            reverse("products:product-list"),
            data=json.dumps({"name": "Monitor", "price": "99.999"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("price", response.json()["errors"])

    def test_updates_and_deletes_product(self):
        product = Product.objects.create(name="Ratón", price="12.00")
        detail_url = reverse("products:product-detail", args=[product.id])

        response = self.client.patch(
            detail_url,
            data=json.dumps({"stock": 4, "active": False}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["stock"], 4)
        self.assertFalse(response.json()["active"])

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Product.objects.filter(pk=product.id).exists())
