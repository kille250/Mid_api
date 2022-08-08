from flask import *
import json
import requests

post_bp = Blueprint('post_bp', __name__, url_prefix="/")


@post_bp.route("/", methods=['GET'])
def home_page():
    return render_template('post/index.html')

@post_bp.route("/process", methods=['POST'])
def send_request():
    test = {
    "value" : request.form.get('value')
    }

    res = requests.post(current_app.config['DOMAIN']+"api/post", data=test)
    arr = json.loads(res.text)
    if res.status_code == 200:
        return redirect(f'/{str(arr["id"])}')
    else:
        #Error Page fehlt.
        return None

@post_bp.route("/<id>", methods=['GET'])
def view(id: str):

    res = requests.get(current_app.config['DOMAIN']+"api/post/"+id)
    arr = json.loads(res.text)

    if arr["status"] == "Finished":
        return render_template('post/render_preview.html', url=arr['file'], text="Image-Processing is done")
    elif arr['status'] == "Error":
        #Error Page is missing
        return None
    elif arr['status'] == "Processing":
        if arr['file'] is None:
            return render_template('post/render_preview.html', reload="refresh", type=5, text="Image-Processing is starting, please wait a while.")
        else:
            return render_template('post/render_preview.html', url=arr['file'], reload="refresh", type=5, text="Processing...")
