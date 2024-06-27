from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from userApp.models import User


class UsersTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(phone_number="+79111113445")
        self.user.verification_code = "1234"
        self.user.save()

    def test_register_user(self):
        data = {
            "phone_number": "+79111113444"
        }
        url = reverse("userApp:user-create")
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            len(response.json()), 1
        )
        users = User.objects.all()
        self.assertEqual(
            len(users), 2
        )

    def test_verify_valid_code(self):
        url = reverse("userApp:user-verify")
        data = {
            "phone_number": self.user.phone_number,
            "code": self.user.verification_code
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_verify_invalid_code(self):
        url = reverse("userApp:user-verify")
        data = {
            "phone_number": self.user.phone_number,
            "code": "79779"
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND
        )



    def test_profile_user(self):
        url = reverse("userApp:user-profile")
        self.client.force_authenticate(self.user)

        response = self.client.get(url)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        data = response.json()

        self.assertEqual(
            data["phone_number"], self.user.phone_number
        )


