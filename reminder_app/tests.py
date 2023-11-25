from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
from .models import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Create your tests here.
class ReminderAndUrlTests(TestCase):
    def setUp(self):
        self.user = Account.objects.create(name="test", email="test@test.test", about="testing")
        self.post = Reminder.objects.create(title="test reminder", date="2023-12-13", description="t e s t", account=self.user)
    
    def test_reminder_content(self):
        self.assertEqual(self.post.title, "test reminder")
        self.assertEqual(self.post.date, "2023-12-13")
        self.assertEqual(self.post.description, "t e s t")
        self.assertEqual(self.post.account, self.user)

    def test_index_url_exists_and_template_correct(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reminder_app/index.html")
        self.assertContains(response, "Start getting organized")

    def test_users_url_exists_and_template_correct(self):
        response = self.client.get(reverse("accounts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reminder_app/account_list.html")
        self.assertContains(response, "test")

# Selenium tests
class NewReminderTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        
    def tearDown(self):
        self.browser.quit()
    
    def test_account_create_and_login(self):
        # navigate to home page
        self.browser.get("http://127.0.0.1:8000")

        # click account registration link
        new_account_link = self.browser.find_element(By.LINK_TEXT, "Click here to create an account")
        new_account_link.click()

        # find input fields
        username_input = self.browser.find_element(By.ID, "id_username")
        email_input = self.browser.find_element(By.ID, "id_email")
        password1_input = self.browser.find_element(By.ID, "id_password1")
        password2_input = self.browser.find_element(By.ID, "id_password2")

        # type in info
        username_input.send_keys('testing')
        email_input.send_keys('test@testing.com')
        password1_input.send_keys('t3stp4ssw0rd')
        password2_input.send_keys('t3stp4ssw0rd')

        # send form
        password2_input.send_keys(Keys.ENTER)
        
        # log in to new user
        self.browser.get("http://127.0.0.1:8000/accounts/login/")
        username_input = self.browser.find_element(By.ID, "id_username")
        password_input = self.browser.find_element(By.ID, "id_password")

        # type login info
        username_input.send_keys('testing')
        password_input.send_keys('t3stp4ssw0rd')
        password_input.send_keys(Keys.ENTER)

        # return to home page
        self.browser.get("http://127.0.0.1:8000")
        logged_in_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertEqual(logged_in_text, "Welcome, testing")

    def test_create_reminder(self):        
        # log in 
        self.browser.get("http://127.0.0.1:8000/accounts/login/")
        username_input = self.browser.find_element(By.ID, "id_username")
        password_input = self.browser.find_element(By.ID, "id_password")

        # type login info
        username_input.send_keys('testing')
        password_input.send_keys('t3stp4ssw0rd')
        password_input.send_keys(Keys.ENTER)

        # return to home page
        self.browser.get("http://127.0.0.1:8000")
        
        # click new reminder button
        new_reminder_label = self.browser.find_element(By.TAG_NAME, "h2")
        new_reminder_button = new_reminder_label.find_element(By.TAG_NAME, "a")

        new_reminder_button.click()

        # find input fields
        title_input = self.browser.find_element(By.ID, "id_title")
        date_input = self.browser.find_element(By.ID, "id_date")
        description_input=self.browser.find_element(By.ID, "id_description")

        # type in info
        title_input.send_keys('test reminder')
        date_input.send_keys('2023-11-24')
        description_input.send_keys('hopefully this works')

        # send form
        submit_button = self.browser.find_element(By.NAME, "Submit")
        submit_button.click()

        # return to home page and check that reminder is there
        self.browser.get("http://127.0.0.1:8000")
        list = self.browser.find_element(By.CLASS_NAME, "list-group")
        reminder_title = list.find_element(By.TAG_NAME, "p").text
        self.assertEqual(reminder_title, "test reminder")