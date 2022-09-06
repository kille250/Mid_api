from flask import *
from db.models.post import Post as tPost
from api.model.post import Post
from api.model.upscale import Upscale
import json
import requests
from functools import wraps

api_bp = Blueprint('api_bp', __name__, url_prefix="/api")

interaction = "https://discord.com/api/v9/interactions"

def validate_request(errlist):
    def container(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            response_err = dict()
            data = request.get_json()
            print(data)
            for i in errlist:
                if i not in data or data[i] == "" or data[i].startswith(" "):
                    response_err[i] = "Invalid"
            if not response_err:
                return fun(*args, **kwargs)
            else:
                print(response_err)
                return response_maker(response_err, 400)
        return wrapper
    return container


def head_builder(key: str):
    header = {
        "Authorization": key
    }

    return header


def make_payload(query: str):
    payload = {
    "type":2,
    "application_id":"936929561302675456",
    "channel_id":"997632760074227732",
    "session_id":"74c811bcf312a5854bc240bc0974fdba",
    "data":{"version":"994261739745050686","id":"938956540159881230", "name":"imagine","type":1,"options":[{"type":3,"name":"prompt", "value":query}]}}

    return payload


def make_payload_up(id: str, image: str):
    payload = {
    "type":3,
    "channel_id":"997632760074227732",
    "message_id":str(id),
    "application_id":"936929561302675456",
    "session_id":"74c811bcf312a5854bc240bc0974fdba",
    "data":{"component_type":2,"custom_id":f"MJ::JOB::upsample::{str(image)}"}}

    return payload


def get_posts():
    mess = requests.get("https://discord.com/api/v9/channels/997632760074227732/messages", headers=head_builder(current_app.config["AUTH"]))
    js = json.loads(mess.text)
    return js


def response_maker(data: dict, code: int):
    response = current_app.response_class(
        response=json.dumps(data),
        status=code,
        mimetype='application/json'
    )
    return response


@api_bp.route("/", methods=['GET'])
def home_page():
    # arr = {}
    # for i in range(len(data)):
    #     arr[i] = data[i].get_data()

    data = tPost.query.all()
    return response_maker(data, 200)


@api_bp.route("/upscale/<id>", methods=['GET'])
def get_upscale_per_id(id: str):
    return None


@api_bp.route("/post/<id>", methods=['GET'])
def get_post_per_id(id: str):

    return None


@api_bp.route("/post", methods=['POST', 'GET'])
@validate_request({"value"})
def post_query():
    query = request.get_json()['value']
    payload = make_payload(query)
    header = head_builder(current_app.config["AUTH"])

    r = requests.post(interaction, json=payload, headers=header)
    print(r.text)
    

    return None


@api_bp.route("/upscale", methods=['GET', 'POST'])
@validate_request({"id", "option"})
def upscale():
    return None
