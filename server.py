import json
import os
from functools import wraps
from flask import Flask, request, jsonify, make_response
from pathlib import Path
import yaml

app = Flask(__name__)

conf = yaml.load(open('conf.yaml'), Loader=yaml.FullLoader)
user = conf['username']
passw = conf['password']

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == user  and auth.password == passw:
            return f(*args, **kwargs)

        return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated


def readJSON(id):
    with open("bots/bot_" + (id) + ".json") as outfile:
        return json.load(outfile)
    outfile.close()




def addJSON(id, payload):
    with open("bots/bot_" + str(id) + ".json", 'w') as outfile:
        return json.dump(payload, outfile, indent=4)


def updateJSON(id):
    payload = request.get_json()
    with open("bots/bot_" + str(id) + ".json", "r") as jsonFile:
        data = json.load(jsonFile)
    for key in payload:
        if key == "provider":
            data["provider"] = payload["provider"]
        elif key == "name":
            data["name"] = payload["name"]
        elif key == "display_name":
            data["display_name"] = payload["display_name"]
        elif key == "credentials":
            data["credentials"] = payload["credentials"]
        else:
            return "Please enter a key to be changed"
        with open("bots/bot_" + str(id) + ".json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=4)
        return "Bot " + Path(str(jsonFile.name)).stem + " has been updated with: " + '\n' + str(payload)


@app.route("/get-bot/<id>")
@auth_required
def getBot(id):
    return readJSON(id)


@app.route("/add-bot", methods=['POST'])
@auth_required
def addBot():
    new_bot = request.get_json()
    id = new_bot.get("id")
    addJSON(id, new_bot)
    return "Bot_" + str(id) + " has been added: " + '\n' + str(new_bot)


@app.route("/put-bot", methods=['PUT'])
@auth_required
def add_or_writeBot():
    new_or_existing_bot = request.get_json()
    id = new_or_existing_bot.get("id")
    addJSON(id, new_or_existing_bot) # This will overwrite an existing json or add a new json file
    return jsonify(new_or_existing_bot)

@app.route("/update/<id>", methods=['PATCH'])
@auth_required
def editBot(id):
    return updateJSON(id)

@app.route("/delete/<id>", methods=['DELETE'])
@auth_required
def removeBot(id=id):
    path = "bots/bot_" + str(id) + ".json"
    if os.path.exists(path):
        os.remove(path)
    return "File " + path + " has been removed"


if __name__ == "__main__": app.run(debug=True)
