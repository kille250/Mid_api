from flask import *
import json
import requests

app = Flask(__name__)

data = {}

header = {
    "Authorization" : ""
}

def tag_builder(tagline: str, inline: str, **kwargs: str):
    str = ""

    str += f'<{tagline}'
    for key, value in kwargs.items():
        str += ' {0}={1}'.format(key, value)
    str += f'>{inline}</{tagline}>'
    return str

def get_posts():
    mess = requests.get("https://discord.com/api/v9/channels/997632760074227732/messages", headers=header)
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


@app.route("/", methods=['GET'])
def home_page():
    return render_template("index.html")

@app.route("/get/<id>", methods=['GET'])
def get_post_per_id(id: int):
    post = get_post(id)
    if post is None:
        if id in data:
            return tag_builder("img", "", src=data[id])+tag_builder("p", "Request is finished processing.")
        else:
            return "Post not found."

    if len(post["attachments"]) != 0:
        url = post["attachments"][0]["url"]
        data[id] = post["attachments"][0]["url"]
        result = tag_builder("img", "", src=url)
        return result+tag_builder("p", "Request is currently processing. It can take a while.")+"<meta http-equiv='refresh' content='5'>"
    else:
        return "Progress will be shown. Reload the Page after a few seconds"+"<meta http-equiv='refresh' content='5'>"

@app.route("/post", methods=['POST', 'GET'])
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
        r = requests.post("https://discord.com/api/v9/interactions", json=payload, headers=header)
        posts = get_posts()
        data[posts[0]["id"]] = (posts[0]["attachments"][0]["url"] if len(posts[0]["attachments"]) != 0 else None)
        button =tag_builder("a",tag_builder("button","Go there to watch the progress"), href=f"'http://167.235.79.2:1337/get/{posts[0]['id']}'")
        return button
    if request.method == 'GET':

        r = requests.post("https://discord.com/api/v9/interactions", json=payload, headers=header)
        posts = get_posts()
        data[posts[0]["id"]] = (posts[0]["attachments"][0]["url"] if len(posts[0]["attachments"]) != 0 else None)
        button =tag_builder("a",tag_builder("button","Go there to watch the progress"), href=f"'http://167.235.79.2:1337/get/{posts[0]['id']}'")
        return button

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337)
