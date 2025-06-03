from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Character


# Create your tests here.
class CharacterAPITestCase(APITestCase):
    def setUp(self):
        # Crear un personaje inicial para pruebas
        self.character1 = Character.objects.create(name="Jonathan", age=182)
        self.character2 = Character.objects.create(name="Mario", age=182)

    def test_get_character_list(self):
        url = reverse('character-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_get_character_detail(self):
        url = reverse('character-detail', args=[self.character1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.character1.name)

    def test_create_character(self):
        url = reverse('character-list')
        data = {"name": "Luigi", "age": 123}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Character.objects.count(), 3)

    def test_delete_character(self):
        url = reverse('character-detail', args=[self.character1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Character.objects.count(), 1)

        url = reverse('character-detail', args=[self.character2.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Character.objects.count(), 0)

    def test_compare_pk_between_objects(self):
        url = reverse('character-detail', args=[self.character1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['name'], self.character2.name)
