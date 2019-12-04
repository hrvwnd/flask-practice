import unittest

from flask import abort, url_for
from flask_testing import TestCase
from os import getenv
from application import app, db
from application.models import Users, Posts, datetime


class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql+pymysql://'+str(getenv('MYSQL_USER'))+':'+str(getenv('MYSQL_PASSWORD'))+'@'+str(getenv('MYSQL_HOST'))+'/'+str(getenv('MYSQL_DB_TEST'))        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.session.commit()
        db.drop_all()
        db.create_all()

        # create test admin user
        admin = Users(first_name="admin", last_name="admin", email="admin@admin.com", password="admin2016")

        # create test non-admin user
        employee = Users(first_name="test", last_name="user", email="test@user.com", password="test2016")

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class FlaskTests(TestBase):

    def test_user_view(self):
        """Tests the user page is inaccessable without logging in and that it re-directs 
        to login page """
        target_url = url_for("account",user_id=2)
        redirect_url = url_for("login", next = target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,redirect_url)


    def test_login_view(self):
        """ Tests login page is accessable when not logged in """
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)
    

    def test_home_view(self):
        """ Tests whether home page is accessable """
        response = self.client.get(url_for("home"))
        self.assertEqual(response.status_code, 200)

    def test_posts_model(self):
        """tests creating a post"""
        post = Posts(title="test",content = "testing this application", date_posted = datetime.utcnow, user_id = 1)
        db.session.add(post)
        db.session.commit()
        self.assertEqual(Posts.query.count(),1)