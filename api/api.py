from flask import *
from api.model.post import Post
from api.model.upscale import Upscale
import json
import requests

api_bp = Blueprint('api_bp', __name__, url_prefix="/api")

data = []

data_up = []

def head_builder(key: str):
    header = {
        "Authorization" : key
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

def get_local_post_by_id(id: str):
    for i in data:
        if i.get_id() == id:
            return i
    return None


def get_post(id: str):
    js = get_posts()
    for i in js:
        if i["id"] == id and get_local_post_by_id(id) != None:
            return i
    return None

def get_post_by_string(inp: str):
    js = get_posts()
    results = [x for x in js if inp in x["content"]]
    return results

def response_maker(data: dict, code: int):
    response = current_app.response_class(
        response=json.dumps(data),
        status=code,
        mimetype='application/json'
    )
    return response

@api_bp.route("/", methods=['GET'])
def home_page():
    arr = {}
    for i in range(len(data)):
        arr[i] = data[i].get_data()
    return response_maker(arr, 200)

@api_bp.route("/post/<id>", methods=['GET'])
def get_post_per_id(id: str):
    post = get_post(id)
    local_post = get_local_post_by_id(id)
    if post is None and local_post is not None:
        if local_post.get_status() != "Finished":
            new_post = get_post_by_string(local_post.get_tag())
            if new_post != None:
                local_post.set_process_id(new_post[0]["id"])
            local_post.set_status("Finished")
        return response_maker(local_post.get_data(), 200)
    elif post is None and local_post is None:
        not_found = Post(status="Not found.")
        return response_maker(not_found.get_data(), 200)

    if len(post["attachments"]) != 0:
        url = post["attachments"][0]["url"]
        local_post.set_file(url)
    return response_maker(local_post.get_data(), 200)


@api_bp.route("/post", methods=['POST', 'GET'])
def post_query():
    response_err = {
        "value": ""
    }
    query = ""
    post = Post()

    if 'value' not in request.args.keys() and 'value' not in request.form.keys():
        response_err["value"] = "Parameter value is missing"
        return response_maker(response_err, 400)
    elif request.form.get('value') is "" or request.args.get('value') is "":
        response_err["value"] = "No input given"
        return response_maker(response_err, 400)
    elif type(request.form.get('value')) is str:
        if request.form.get('value').startswith(" "):
            response_err["value"] = "Invalid Input"
            return response_maker(response_err, 400)
    elif type(request.args.get('value')) is str:
        if request.args.get('value').startswith(" "):
            response_err["value"] = "Invalid Input"
            return response_maker(response_err, 400)

    if len(request.form) != 0:
        query = request.form.get('value')
    elif len(request.args) != 0:
        query = request.args.get('value')

    payload = make_payload(query)

    if request.method == 'POST' or request.method == 'GET':
        r = requests.post("https://discord.com/api/v9/interactions", json=payload, headers=head_builder(current_app.config["AUTH"]))
        print(r.text)
        posts = get_posts()
        post.set_id(posts[0]["id"])
        post.set_tag(query)
        post.set_file((posts[0]["attachments"][0]["url"] if len(posts[0]["attachments"]) != 0 else None))
        post.set_status("Processing")
        data.append(post)
        domain = current_app.config['IP']
        return response_maker(post.get_data(), 200)

@api_bp.route("/upscale/<id>/<option>", methods=['GET', 'POST'])
def upscale(id: str, option: str):
    post = get_local_post_by_id(id)
    upscale = Upscale()
    if post is not None:
        if option.isdigit() and int(option) <= 4 and int(option) != 0:
            payload = make_payload_up(post.get_process_id(), option)
            r = requests.post("https://discord.com/api/v9/interactions", json=payload, headers=head_builder(current_app.config["AUTH"]))
            posts = get_posts()
            upscale.set_id(posts[0]["id"])
            upscale.set_status("Processing")
            upscale.set_file((posts[0]["attachments"][0]["url"] if len(posts[0]["attachments"]) != 0 else None))
            data_up.append(upscale)
            domain = current_app.config['IP']
            return response_maker(upscale.get_data(), 200)
