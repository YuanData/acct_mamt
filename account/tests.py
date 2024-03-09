from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AccountTests(APITestCase):
    def test_create_account_success(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('account-create')
        data = {'username': 'newuser', 'password': 'Password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['success'], True)

    def test_verify_account_success(self):
        """
        Ensure we can successfully verify an account.
        """
        # First, create an account
        create_url = reverse('account-create')
        create_data = {'username': 'user1', 'password': 'Password123'}
        self.client.post(create_url, create_data, format='json')

        # Then, verify the account
        verify_url = reverse('account-verify')
        verify_data = {'username': 'user1', 'password': 'Password123'}
        response = self.client.post(verify_url, verify_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)

    def test_verify_account_failure(self):
        # First, create an account
        create_url = reverse('account-create')
        create_data = {'username': 'user2', 'password': 'Password123'}
        self.client.post(create_url, create_data, format='json')

        # Then, verify the account
        verify_url = reverse('account-verify')
        verify_data = {'username': 'user2', 'password': 'WrongPassword'}
        response = self.client.post(verify_url, verify_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['success'], False)

    def test_too_many_failed_attempts(self):
        verify_url = reverse('account-verify')
        data = {'username': 'testuser', 'password': 'WrongPassword!'}
        for _ in range(5):
            self.client.post(verify_url, data, format='json')
        response = self.client.post(verify_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertEqual(response.data['success'], False)
        self.assertIn("Too many failed login attempts", response.data['reason'])
