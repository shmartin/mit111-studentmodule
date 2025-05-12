from django.test import TestCase
from django.urls import reverse

class HelpPageTest(TestCase):
    def test_help_page_status_code(self):
        response = self.client.get(reverse('help'))
        self.assertEqual(response.status_code, 200)

    def test_help_page_template_used(self):
        response = self.client.get(reverse('help'))
        self.assertTemplateUsed(response, 'submission/help.html')
