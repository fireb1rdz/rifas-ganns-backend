from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Raffle, RafflePicture

class RaffleViewSetTests(APITestCase):
    def create_image(self, name="test.jpg"):
        return SimpleUploadedFile(
            name, b"file_content", content_type="image/jpeg"
        )

    def test_create_raffle_with_images(self):
        url = "/api/raffles/"
        data = {
            "title": "Rifa Teste",
            "description": "Descrição de teste",
            "pictures": [
                self.create_image("img1.jpg"),
                self.create_image("img2.jpg"),
            ]
        }

        response = self.client.post(url, data, format="multipart")

        # ✅ Deve criar com sucesso
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Raffle.objects.count(), 1)
        self.assertEqual(RafflePicture.objects.count(), 2)

        raffle = Raffle.objects.first()
        self.assertEqual(raffle.title, "Rifa Teste")
        self.assertEqual(raffle.pictures.count(), 2)

    def test_create_raffle_without_images(self):
        url = "/api/raffles/"
        data = {
            "title": "Rifa Sem Imagem",
            "description": "Teste sem imagens",
            "pictures": []
        }

        response = self.client.post(url, data, format="multipart")

        # ✅ Deve criar a rifa mesmo sem imagens
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Raffle.objects.count(), 1)
        self.assertEqual(RafflePicture.objects.count(), 0)

    def test_list_raffles(self):
        raffle = Raffle.objects.create(title="Rifa Listada", description="teste")
        RafflePicture.objects.create(raffle=raffle, image=self.create_image("img.jpg"))

        url = "/api/raffles/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Rifa Listada")
        self.assertEqual(len(response.data[0]["images"]), 1)
