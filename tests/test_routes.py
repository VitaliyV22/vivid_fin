import pytest
from flask import url_for

def test_index_route_authenticated(client, app):
    with app.test_request_context():
        response = client.get(url_for('main.index'))
        assert response.status_code == 200

def test_index_route_unauthenticated(client, app):
    with app.test_request_context():
        response = client.get(url_for('main.index'), follow_redirects=True)
        assert response.status_code == 200
        assert b'Please log in to access this page.' in response.data

def test_login_route(client, app):
    with app.test_request_context():
        response = client.get(url_for('main.login'))
        assert response.status_code == 200

def test_logout_route(client, app):
    with app.test_request_context():
        response = client.get(url_for('main.logout'))
        assert response.status_code == 302
        assert response.location == url_for('main.index', _external=True)

def test_register_route(client, app):
    with app.test_request_context():
        response = client.get(url_for('main.register'))
        assert response.status_code == 200
