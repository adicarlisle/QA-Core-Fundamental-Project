from flask import url_for
from flask_testing import TestCase, LiveServerTestCase
from werkzeug.wrappers.response import Response
from application import app, db
from application.models import Users, Dice, History
from selenium import webdriver
from urllib.request import urlopen
class TestBase(TestCase):
    def create_app(self):
        app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///",
                SECRET_KEY='TEST_SECRET_KEY',
                DEBUG=True,
                WTF_CSRF_ENABLED=False,
                LOGIN_DISABLED=True
                )
        
        return app
    
    def setUp(self):        
        db.create_all()
        author = Users(
            username="Adi",
            email = "test@email.test",
            password = "password",
            )
        die = Dice(
            level=2,
            range=10
        )
        entry = History(
            user_id = 1,
            dice_id = 1,
            value = 20
        )
        db.session.add(author)
        db.session.add(die)
        db.session.add(entry)
        db.session.commit()
        
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestViews(TestBase):
    def test_get_home(self):
        response = self.client.get(url_for("home"))
        self.assert200(response, "Failed to load homepage")

    def test_get_register(self):
        response = self.client.get(url_for("register"))
        self.assert200(response, "Failed to load register page")

    def test_post_register_valid(self):
        response = self.client.post(url_for("register"), data=dict(
            username="test",
            email="test@email.com",
            password="12345678"

        ))
        self.assert200(response, "Failed to register with valid details")

    def test_post_register_invalid(self):
        response = self.client.post(url_for("register"), data=dict(
            username="test",
            email="test@email.com",
            password="1"

        ))
        self.assert200(response, "Failed to register with invalid details")

    def test_get_login(self):
        response = self.client.get(url_for("login"))
        self.assert200(response, "Failed to load login page")

    def test_post_login_valid(self):
        response = self.client.post(url_for("login"), data=dict(
            username="test",
            email="test@email.com",
            password="12345678"

        ))
        self.assert200(response, "Failed to log in with valid details")

    
    def test_post_login_invalid(self):
        response = self.client.post(url_for("login"), data=dict(
            username="test",
            email="test@email.com",
            password="1"

        ))
        self.assert200(response, "Failed to log in with invalid details")

    def test_get_dashboard(self):
        response = self.client.get(url_for("dashboard"))
        self.assert200(response, "Failed to load dashboard")

    def test_post_dashboard(self):
        response = self.client.post(url_for("dashboard"), data=dict(
            level="2",
            range="10",
        ))
        self.assert200(response, "Failed to POST to dashboard")

    
    # def test_get_reset_dice(self):
    #     response = self.client.get(url_for("reset_dice", id="1"))
    #     self.assert200(response, "Failed to reset dice")
    
    def test_get_reset_history(self):
        response = self.client.get(url_for("reset_history"))
        self.assert_status(response, 302, "Failed to redirect after history reset")

    def test_get_update(self):
        response = self.client.get(url_for("update", id="1"))
        self.assert200(response, "Failed to update dice")

    def test_post_update(self):
        response = self.client.post(url_for("update",id="1"), data=dict(
            level="9",
            range="10"
        ))
        self.assert_status(response, 302, "Failed to redirect after update")

    def test_redirect_logout(self):
        response = self.client.get(url_for("logout"))
        self.assert_status(response, 302, "Failed to redirect after log out")

    # def test_get_roll(self):
    #     response = self.client.get(url_for("roll", dice="1"))
    #     self.assert200(response, "Failed to add entry to history")

class SeleniumTests(LiveServerTestCase):
    TEST_PORT = 5050

    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI="sqlite:///",
            LIVESERVER_PORT=self.TEST_PORT,

            DEBUG=True,
            TESTING=True

        )
        return app

    def setUp(self):
        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

        db.create_all()

        self.driver.get(f'http://localhost:{self.TEST_PORT}')

    def tearDown(self):
        self.driver.quit()

        db.drop_all()

    def test_live(self):
        response = urlopen(f'http://localhost:{self.TEST_PORT}')
        self.assertEqual(response.code, 200)

class TestLive(SeleniumTests):
    def test_live_full_usage(self):
        correct_user_username ="test"
        correct_user_email = "test@abracadabra.com"
        correct_user_password = "1234567890"
        self.driver.find_element_by_xpath('//*[@id="button1"]/form/button').click()
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(correct_user_username)
        self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(correct_user_email)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(correct_user_password)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        self.driver.find_element_by_css_selector('#button2 > form > button').click()
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(correct_user_username)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(correct_user_password)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()

        text = self.driver.find_element_by_xpath('//*[@id="welcomeMessage"]')
        self.assertEqual(text, f'Hello {correct_user_username}')

        

