from django.test import TestCase
from django.urls import reverse
from .models import *

# Create your tests here.
class ReminderAndUrlTests(TestCase):
    def setUp(self):
        self.user = Account.objects.create(name="test", email="test@test.test", about="testing")
        self.post = Reminder.objects.create(title="test reminder", date="2023-12-13", description="t e s t", account=self.user)
    
    def test_reminder_content(self):
        self.assertEqual(self.post.title, "test reminder")
        self.assertEqual(self.post.date, "2023-12-13")
        self.assertEqual(self.post.description, "t e s t")
        self.assertEqual(self.post.user, self.user)

    def test_index_url_exists_and_template_correct(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reminder_app/index.html")
        self.assertContains(response, "Your Reminders")

    def test_users_url_exists_and_template_correct(self):
        response = self.client.get(reverse("accounts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reminder_app/account_list.html")
        self.assertContains(response, "test")
    