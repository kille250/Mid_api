from flask import *
import json
import requests

api_bp = Blueprint('api_bp', __name__, url_prefix="/api")

data = {}

def head_builder(key: str):
    header = {
        "Authorization" : key
    }

    return header


def get_posts():
    mess = requests.get("https://discord.com/api/v9/channels/997632760074227732/messages", headers=head_builder(current_app.config["AUTH"]))
    js = json.loads(mess.text)
    return js


def get_post(id: int):
    js = get_posts()
    for i in js:
        if i["id"] == id and str(id) in data:
            return i
    return None

def make_payload(query: str):
    payload = {
    "type":2,
    "application_id":"936929561302675456",
    "channel_id":"997632760074227732",
    "session_id":"3692231aa5c9730e1fdf7af65186e4ce",
    "data":{"version":"994261739745050686","id":"938956540159881230", "name":"imagine","type":1,"options":[{"type":3,"name":"prompt", "value":query}]}
    }

    return payload


@api_bp.route("/", methods=['GET'])
def home_page():
    return render_template("index.html")


@api_bp.route("/post/<id>", methods=['GET'])
def get_post_per_id(id: int):
    post = get_post(id)
    if post is None:
        if id in data:
            return render_template('render_preview.html', url=data[id], text="Task finished.")
        else:
            return "Post not found."

    if len(post["attachments"]) != 0:
        url = post["attachments"][0]["url"]
        data[id] = url
        return render_template('render_preview.html', url=url, reload="refresh", type=5, text="Image-Generation will take a while. Please be patiend.")
    else:
        return render_template('render_preview.html',reload="refresh", type=5, text="Process will start, wait a moment.")


@api_bp.route("/", methods=['POST', 'GET'])
def post_query():
    query = ""

    if 'value' not in request.args.keys() and 'value' not in request.form.keys():
        return "Parameter Value is missing"
    elif request.form.get('value') is "" or request.args.get('value') is "":
        return "No Input, try again."
    elif type(request.form.get('value')) is str:
        if request.form.get('value').startswith(" "):
            return "Remove the space from the beginning."
    elif type(request.args.get('value')) is str:
        if request.args.get('value').startswith(" "):
            return "Remove the space from the beginning."

    if len(request.form) != 0:
        query = request.form.get('value')
    elif len(request.args) != 0:
        query = request.args.get('value')

    payload = make_payload(query)

    if request.method == 'POST':
        r = requests.post("https://discord.com/api/v9/interactions", json=payload, headers=head_builder(current_app.config["AUTH"]))
        posts = get_posts()
        data[posts[0]["id"]] = (posts[0]["attachments"][0]["url"] if len(posts[0]["attachments"]) != 0 else None)
        domain = current_app.config['IP']
        return redirect("post/"+posts[0]["id"])
    if request.method == 'GET':
        r = requests.post("https://discord.com/api/v9/interactions", json=payload, headers=head_builder(current_app.config["AUTH"]))
        posts = get_posts()
        data[posts[0]["id"]] = (posts[0]["attachments"][0]["url"] if len(posts[0]["attachments"]) != 0 else None)
        domain = current_app.config['IP']
        return redirect("post/"+posts[0]["id"])
