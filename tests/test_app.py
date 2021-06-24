from flask import url_for
from flask_testing import TestCase
from application import app, db
from application.models import Users, Dice, History

class TestBase(TestCase):
    def create_app(self):
        app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///",
                SECRET_KEY='TEST_SECRET_KEY',
                DEBUG=True,
                WTF_CSRF_ENABLED=False
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
            dice_id = 1
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

    def test_get_login(self):
        response = self.client.get(url_for("login"))
        self.assert200(response, "Failed to load login page")
