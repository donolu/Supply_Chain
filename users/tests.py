from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from users.models import Profile


class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.profile = Profile.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            bio="Lorem ipsum dolor sit amet.",
        )
        self.login_url = reverse("login")
        self.profile_url = reverse("profile")

    def test_profile_page(self):
        # Ensure the profile page is accessible to authenticated users
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John")  # Make sure the first name is displayed
        self.assertContains(response, "Doe")  # Make sure the last name is displayed
        self.assertContains(
            response, "Lorem ipsum dolor sit amet."
        )  # Make sure the bio is displayed

    def test_profile_page_redirect_for_unauthenticated_users(self):
        # Ensure unauthenticated users are redirected to the login page
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, self.login_url + "?next=" + self.profile_url)
