"""
REST API module tests - run against https://reqres.in (public fake REST API)
"""

import requests
from jsonschema import validate, ValidationError
from conftest import attach_context
import os
from dotenv import load_dotenv
load_dotenv()


BASE_URL = "https://reqres.in/api"

HEADERS = {"x-api-key": os.environ.get("REQRES_API_KEY", "")}
USER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "email": {"type": "string"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
    },
    "required": ["id", "email", "first_name", "last_name"],
}


def test_auth_token_validation_success(request):
    resp = requests.post(
        f"{BASE_URL}/login",
        json={"email": "eve.holt@reqres.in", "password": "cityslicka"},
        headers=HEADERS,
    )
    attach_context(request, request_url=resp.url, status_code=resp.status_code, response_body=resp.text)
    assert resp.status_code == 200
    assert "token" in resp.json()


def test_auth_token_validation_missing_password_returns_400(request):
    resp = requests.post(
        f"{BASE_URL}/login",
        json={"email": "eve.holt@reqres.in"},
        headers=HEADERS,
    )
    attach_context(request, request_url=resp.url, status_code=resp.status_code, response_body=resp.text)
    assert resp.status_code == 400
    assert "error" in resp.json()


def test_crud_create_user(request):
    resp = requests.post(
        f"{BASE_URL}/users",
        json={"name": "morpheus", "job": "leader"},
        headers=HEADERS,
    )
    attach_context(request, request_url=resp.url, status_code=resp.status_code, response_body=resp.text)
    assert resp.status_code == 201
    assert resp.json()["name"] == "morpheus"


def test_crud_read_single_user(request):
    resp = requests.get(f"{BASE_URL}/users/2", headers=HEADERS)
    attach_context(request, request_url=resp.url, status_code=resp.status_code, response_body=resp.text)
    assert resp.status_code == 200
    assert "data" in resp.json()


def test_crud_update_user(request):
    resp = requests.put(
        f"{BASE_URL}/users/2",
        json={"name": "morpheus", "job": "zion resident"},
        headers=HEADERS,
    )
    attach_context(request, request_url=resp.url, status_code=resp.status_code, response_body=resp.text)
    assert resp.status_code == 200
    assert resp.json()["job"] == "zion resident"


def test_crud_delete_user(request):
    resp = requests.delete(f"{BASE_URL}/users/2", headers=HEADERS)
    attach_context(request, request_url=resp.url, status_code=resp.status_code)
    assert resp.status_code == 204


def test_error_handling_user_not_found_returns_404(request):
    resp = requests.get(f"{BASE_URL}/users/23000", headers=HEADERS)
    attach_context(request, request_url=resp.url, status_code=resp.status_code, response_body=resp.text)
    assert resp.status_code == 404


def test_schema_validation_user_object(request):
    resp = requests.get(f"{BASE_URL}/users/2", headers=HEADERS)
    body = resp.json()["data"]
    attach_context(request, request_url=resp.url, status_code=resp.status_code, response_body=str(body))
    try:
        validate(instance=body, schema=USER_SCHEMA)
    except ValidationError as e:
        raise AssertionError(f"Schema validation failed: {e.message}")