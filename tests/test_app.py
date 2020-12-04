import pytest
import logging

from flaskblog import app, db, bcrypt
from flaskblog.models import User
from flask_login import login_user, current_user, logout_user, login_required


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client


def test_home_route(client):
    rv = client.get("/home")
    print("rv : ", rv.data)
    assert 200 == rv.status_code
    # assertTemplateUsed(response, 'template_name.html')


def test_about_route(client):
    rv = client.get("/about")
    print("rv : ", rv.data)
    assert 200 == rv.status_code
    # assertTemplateUsed(response, 'template_name.html')


def test_login(client):
    hashed_password = bcrypt.generate_password_hash('12345').decode('utf-8')
    user = User(username='janedo', email='janedo.1999@gmail.com',
                password=hashed_password)
    db.session.add(user)
    # db.session.commit()
    rv = client.post('/login',
                     data=dict(email="janedo.1999@gmail.com",
                               password="12345"),
                     follow_redirects=True
                     )
    print("rv : ", rv.status)
    # print("cU : ", current_user.is_authenticated)
    # print("rv : ", rv.path)
    # assertRedirects(rv,url_for('/home'))
    #  url_for('home.html'))
    assert 200 == rv.status_code
    # assertRedirects(res, url_for('home.html'))
    db.session.delete(user)
    db.session.commit()


def test_login_page_loads(client):
    rv = client.get('/login')
    # print(rv.data);
    assert b'Log In' in rv.data


def test_incorrect_login(client):
    hashed_password = bcrypt.generate_password_hash('12345').decode('utf-8')
    user = User(username='janedo', email='janedo.1999@gmail.com',
                password=hashed_password)
    db.session.add(user)
    # db.session.commit()
    rv = client.post('/login',
                     data=dict(email="janedo.1269@gmail.com", password="123"),
                     follow_redirects=True
                     )
    # print("rv : ", rv)
    # print("rv : ", rv.path)
    # assertRedirects(rv,url_for('/home'))
    #  url_for('home.html'))
    assert 201 == rv.status_code
    assert b'Login Unsuccessful. Please check email and password' in rv.data
    # assertRedirects(res, url_for('home.html'))
    db.session.delete(user)
    db.session.commit()


def test_logout(client):
    rv = client.get('/logout',
                    follow_redirects=True
                    )
    print("rv : ", rv.data)
    assert 200 == rv.status_code


def test_register_page_loads(client):
    rv = client.get('/register')
    # print(rv.data);
    assert b'Join Today' in rv.data


def test_register(client):
    rv = client.post('/register',
                     data=dict(username="janedo", email="janedo.1999@gmail.com",
                               password="12345", confirm_password="12345"),
                     follow_redirects=True
                     )
    assert 201 == rv.status_code
    print("rv : ", rv.data)
    assert b'Your account has been created! You are now able to log in' in rv.data
    user = User.query.filter_by(email="janedo.1999@gmail.com").first()
    db.session.delete(user)
    db.session.commit()


def test_incorrect_register1(client):
    rv = client.post('/register',
                     data=dict(username="janedo", email="janedo.1999@gmail.com",
                               password="12345", confirm_password="12445"),
                     follow_redirects=True
                     )
    assert 201 == rv.status_code
    print("rv : ", rv.data)
    assert b'Bloginator - Register' in rv.data
    user = User.query.filter_by(email="janedo.1999@gmail.com").first()
    if(user):
        db.session.delete(user)
        db.session.commit()


def test_incorrect_register2(client):
    rv = client.post('/register',
                     data=dict(username="janedo", email="janedo.1999@gmailcom",
                               password="12345", confirm_password="12445"),
                     follow_redirects=True
                     )
    assert 201 == rv.status_code
    print("rv : ", rv.data)
    assert b'Bloginator - Register' in rv.data
    user = User.query.filter_by(email="janedo.1999@gmailcom").first()
    if(user):
        db.session.delete(user)
        db.session.commit()


def test_add_post(client):
    # Login User
    hashed_password = bcrypt.generate_password_hash('12345').decode('utf-8')
    user = User(username='janedo', email='janedo.1999@gmail.com',
                password=hashed_password)
    db.session.add(user)
    db.session.commit()
    rv = client.post('/login',
                     data=dict(email="janedo.1999@gmail.com",
                               password="12345"),
                     follow_redirects=True
                     )
    # Add Post
    rv = client.post('/post/new',
                     data=dict(title="TestPost", content="Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."),
                     follow_redirects=True
                     )
    user = User.query.filter_by(email="janedo.1999@gmail.com").first()
    # db.session.delete(user)
    # db.session.commit()
    print(rv)
    print(rv.data)
    assert 200 == rv.status_code


def test_one_post(client):
    # Login User
    hashed_password = bcrypt.generate_password_hash('12345').decode('utf-8')
    user = User(username='janedo1', email='janedo1.1999@gmail.com',
                password=hashed_password)
    db.session.add(user)
    db.session.commit()
    rv = client.post('/login',
                     data=dict(email="janedo1.1999@gmail.com",
                               password="12345"),
                     follow_redirects=True
                     )
    # View Post
    rv = client.get('/post/3',
                    data=dict(title="TestPost", content="Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."),
                    follow_redirects=True
                    )
    assert 200 == rv.status_code
