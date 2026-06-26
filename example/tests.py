import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from example.models import Article, Category, Customer, Tag


GIF_IMAGE = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
    b"\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,"
    b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02"
    b"D\x01\x00;"
)


class TemporaryMediaRootMixin:

    @classmethod
    def setUpClass(cls):
        cls._media_root = tempfile.TemporaryDirectory()
        cls._media_override = override_settings(MEDIA_ROOT=cls._media_root.name)
        cls._media_override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls._media_override.disable()
        cls._media_root.cleanup()


class CustomerExampleFlowTests(TestCase):
    databases = {"default", "example"}

    def test_customer_create_detail_and_update_flow(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Customer form")

        response = self.client.post(reverse("index"), {
            "name": "Ada Lovelace",
            "color": "#0f9f7d",
            "radio": "5",
        })
        self.assertRedirects(response, reverse("index"))

        customer = Customer.objects.get(name="Ada Lovelace")
        self.assertEqual(customer.color, "#0F9F7D")

        response = self.client.get(reverse("customer_detail", args=[customer.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ada Lovelace")

        response = self.client.post(reverse("customer_update", args=[customer.pk]), {
            "name": "Ada Byron",
            "color": "#224466",
            "radio": "4",
        })
        self.assertRedirects(response, reverse("customer_detail", args=[customer.pk]))

        customer.refresh_from_db()
        self.assertEqual(customer.name, "Ada Byron")
        self.assertEqual(customer.color, "#224466")

    def test_generated_customer_crud_list_is_reachable(self):
        Customer.objects.create(name="Grace Hopper", color="#112233")

        response = self.client.get("/views/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Grace Hopper")


class JsonExampleFlowTests(TestCase):

    def test_json_views_round_trip_payloads(self):
        response = self.client.get("/json/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"json": True})

        response = self.client.post(
            "/json/post/",
            data=b'{"status": "ok"}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_content_type_guard_returns_415(self):
        response = self.client.get(reverse("content_type"))

        self.assertEqual(response.status_code, 415)


class ArticleExampleFlowTests(TemporaryMediaRootMixin, TestCase):
    databases = {"default", "example"}

    def test_article_crud_and_deleted_archive_flow(self):
        category = Category.objects.create(name="News")
        tag = Tag.objects.create(
            name="Release",
            category=category,
            color="#123456",
        )

        response = self.client.get(reverse("article_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No articles yet")

        response = self.client.post(reverse("article_create"), {
            "title": "Typed example app",
            "text": "The example app exercises django-boost integrations.",
            "tags": [str(tag.pk)],
            "image": SimpleUploadedFile("article.gif", GIF_IMAGE, "image/gif"),
        })
        self.assertRedirects(response, reverse("article_list"))

        article = Article.objects.get(title="Typed example app")
        self.assertEqual(list(article.tags.values_list("name", flat=True)), ["Release"])

        response = self.client.get(reverse("article_detail", args=[article.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Typed example app")

        response = self.client.post(reverse("article_update", args=[article.pk]), {
            "title": "Typed example app updated",
            "text": "The update view keeps the sample executable.",
            "tags": [str(tag.pk)],
        })
        self.assertRedirects(response, reverse("article_list"))

        article.refresh_from_db()
        self.assertEqual(article.title, "Typed example app updated")

        response = self.client.get(reverse("article_delete", args=[article.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete article")

        response = self.client.post(reverse("article_delete", args=[article.pk]))
        self.assertRedirects(response, reverse("article_list"))

        article.refresh_from_db()
        self.assertTrue(article.is_dead())

        response = self.client.get(reverse("article_deleted_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Typed example app updated")
