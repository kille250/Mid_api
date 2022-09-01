from flask import *
from flask_login import login_required
import json
import requests

post_bp = Blueprint('post_bp', __name__)


@post_bp.route("/", methods=['GET'])
@login_required
def home_page():
    return render_template('post/index.html')


@post_bp.route("/process", methods=['POST'])
@login_required
def send_request():
    test = {
    "value" : request.form.get('value')
    }

    res = requests.post(current_app.config['DOMAIN']+"api/post", json=test)
    arr = json.loads(res.text)
    if res.status_code == 200:
        return redirect(url_for("post_bp.view", id=arr["id"]))
    elif res.status_code == 400:
        #Error Page fehlt.
        return arr


@post_bp.route("/<id>/<option>", methods=['GET', 'POST'])
@login_required
def upscale(id: str, option: str):
    test = {
    "id" : id,
    "option" : option
    }
    res = requests.post(current_app.config['DOMAIN']+"api/upscale", json=test)
    arr = json.loads(res.text)
    return redirect(url_for("post_bp.view_upscale", id=str(arr["id"])))


@post_bp.route("/upscale/<id>", methods=['GET'])
@login_required
def view_upscale(id: str):

    res = requests.get(current_app.config['DOMAIN']+"api/upscale/"+id)
    arr = json.loads(res.text)

    if arr["status"] == "Finished":
        return render_template('post/render_preview.html', url=arr['file'], text="Image-Processing is done", domain=url_for("post_bp.home_page"), fin=False)
    elif arr['status'] == "Not found.":
        #Error Page is missing
        return arr
    elif arr['status'] == "Processing":
        if arr['file'] is None:
            return render_template('post/render_preview.html', reload="refresh", type=5, text="Image-Processing is starting, please wait a while.", domain=url_for("post_bp.home_page"), fin=False)
        else:
            return render_template('post/render_preview.html', url=arr['file'], reload="refresh", type=5, text="Processing...", domain=url_for("post_bp.home_page"), fin=False)


@post_bp.route("/<id>", methods=['GET'])
@login_required
def view(id: str):

    res = requests.get(current_app.config['DOMAIN']+"api/post/"+id)
    arr = json.loads(res.text)

    if arr["status"] == "Finished":
        return render_template('post/render_preview.html', url=arr['file'], text="Image-Processing is done", domain=url_for("post_bp.home_page"), fin=True, u1=url_for("post_bp.upscale", id=id, option=1), u2=url_for("post_bp.upscale", id=id, option=2), u3=url_for("post_bp.upscale", id=id, option=3), u4=url_for("post_bp.upscale", id=id, option=1))
    elif arr['status'] == "Not found.":
        #Error Page is missing
        return arr
    elif arr['status'] == "Processing":
        if arr['file'] is None:
            return render_template('post/render_preview.html', reload="refresh", type=5, text="Image-Processing is starting, please wait a while.", domain=url_for("post_bp.home_page"), fin=False)
        else:
            return render_template('post/render_preview.html', url=arr['file'], reload="refresh", type=5, text="Processing...", domain=url_for("post_bp.home_page"), fin=False)
