from pip._vendor import requests
import json
import yaml
from pip._vendor.requests.auth import HTTPBasicAuth

conf = yaml.load(open('conf.yaml'), Loader=yaml.FullLoader)
user = conf['username']
passw = conf['password']

def test_get(id=2):
    response = requests.get("http://127.0.0.1:5000/get-bot/" + str(id), auth=HTTPBasicAuth(user, passw))
    json = {
        "credentials": "Hostname: localhost; Port: 5000",
        "display_name": "Bot #1",
        "id": str(id),
        "name": "ACBOT_1",
        "provider": "TARS"
    }
    assert response.status_code == 200
    assert response.json() == json


def test_post(id):
    data = {
        "id": str(id),
        "provider": "TARS",
        "name": "ACBOT_1",
        "display_name": "Bot #1",
        "credentials": "Hostname: localhost; Port: 5000"
    }
    url = "http://127.0.0.1:5000/add-bot"
    request = requests.post(url, json=data, auth=HTTPBasicAuth(user, passw))
    with open('bots/bot_8.json', 'w') as outfile:
         return json.dump(data, outfile, indent=4)
    assert request.status_code == 200
    assert outfile.read == data


def test_put_o(id):  # Overites
    data = {"credentials": "Hostname: localhost; Port: 5000", "display_name": "Bot #1", "id": str(id), "name": "ACBOT_1", "provider": "TARS"}
    url = "http://127.0.0.1:5000/put-bot"
    put_request = requests.put(url, json=data, auth=HTTPBasicAuth(user, passw))
    put_response = put_request.json()
    assert put_request.status_code == 200
    assert put_response == data


def test_put_in(id=808):    # Inserts/ Adds
    data = {"credentials": "Hostname: localhost; Port: 5000", "display_name": "Bot #1", "id": str(id), "name": "ACBOT_1", "provider": "TARS"}
    url = "http://127.0.0.1:5000/put-bot"
    put_request = requests.put(url, json=data, auth=HTTPBasicAuth(user, passw))
    put_response = put_request.json()
    url_delete = "http://127.0.0.1:5000/delete/" + str(id)
    requests.delete(url_delete, auth=HTTPBasicAuth(user, passw))
    assert put_request.status_code == 200
    assert put_response == data


def test_patch(id):
    data = {"credentials": "new credentials"}
    url = "http://127.0.0.1:5000/update/" + str(id)
    patch_request = requests.patch(url, json=data, auth=HTTPBasicAuth(user, passw))
    assert patch_request.status_code == 200
    assert patch_request.text == "Bot bot_" +str(id) + " has been updated with: " + '\n' + str(data)


def test_delete(id=999):  # This is creating a new bot under bot_999.json and then deleting it after
    data = {
        "id": str(id),
        "provider": "TARS",
        "name": "ACBOT_1",
        "display_name": "Bot #1",
        "credentials": "Hostname: localhost; Port: 5000"
    }
    url = "http://127.0.0.1:5000/add-bot"
    requests.post(url, json=data, auth=HTTPBasicAuth(user, passw))
    url_delete = "http://127.0.0.1:5000/delete/" + str(id)
    delete_request = requests.delete(url_delete, auth=HTTPBasicAuth(user, passw))
    assert delete_request.status_code == 200


def test_auth():
    response = requests.get("http://127.0.0.1:5000/get-bot/" + str(id))   # Send request with no auth
    json = {
        "credentials": "Hostname: localhost; Port: 5000",
        "display_name": "Bot #1",
        "id": str(id),
        "name": "ACBOT_1",
        "provider": "TARS"
    }
    assert response.status_code == 401   # Should return 401 Unauthorized client.....