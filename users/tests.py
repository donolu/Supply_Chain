from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.


class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
            first_name="John",
            last_name="Doe",
        )

    def test_profile_page(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Retrieve the profile page URL using the named URL pattern
        url = reverse("profile")

        # Send a GET request to the profile page URL
        response = self.client.get(url)

        # Check that the response has a status code of 200 (successful)
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the user's first name
        self.assertContains(response, "John")

        # Check that the response contains the user's last name
        self.assertContains(response, "Doe")

        # Check that the response contains the user's email
        self.assertContains(response, "test@example.com")
