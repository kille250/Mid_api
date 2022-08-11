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

    res = requests.post(current_app.config['DOMAIN']+"api/post", json=test)
    arr = json.loads(res.text)
    if res.status_code == 200:
        return redirect(f'/{str(arr["id"])}')
    elif res.status_code == 400:
        #Error Page fehlt.
        return arr

@post_bp.route("/<id>/<option>", methods=['GET', 'POST'])
def upscale(id: str, option: str):
    test = {
    "id" : id,
    "option" : option
    }
    res = requests.post(current_app.config['DOMAIN']+"api/upscale", json=test)
    arr = json.loads(res.text)
    return redirect(f'/upscale/{str(arr["id"])}')

@post_bp.route("/upscale/<id>", methods=['GET'])
def view_upscale(id: str):

    res = requests.get(current_app.config['DOMAIN']+"api/upscale/"+id)
    arr = json.loads(res.text)

    if arr["status"] == "Finished":
        return render_template('post/render_preview.html', url=arr['file'], text="Image-Processing is done", domain=current_app.config['DOMAIN'], fin=False)
    elif arr['status'] == "Not found.":
        #Error Page is missing
        return arr
    elif arr['status'] == "Processing":
        if arr['file'] is None:
            return render_template('post/render_preview.html', reload="refresh", type=5, text="Image-Processing is starting, please wait a while.", domain=current_app.config['DOMAIN'], fin=False)
        else:
            return render_template('post/render_preview.html', url=arr['file'], reload="refresh", type=5, text="Processing...", domain=current_app.config['DOMAIN'], fin=False)

@post_bp.route("/<id>", methods=['GET'])
def view(id: str):

    res = requests.get(current_app.config['DOMAIN']+"api/post/"+id)
    arr = json.loads(res.text)

    if arr["status"] == "Finished":
        return render_template('post/render_preview.html', url=arr['file'], text="Image-Processing is done", domain=current_app.config['DOMAIN'], fin=True, u1=current_app.config['DOMAIN']+id+"/1", u2=current_app.config['DOMAIN']+id+"/2", u3=current_app.config['DOMAIN']+id+"/3", u4=current_app.config['DOMAIN']+id+"/4")
    elif arr['status'] == "Not found.":
        #Error Page is missing
        return arr
    elif arr['status'] == "Processing":
        if arr['file'] is None:
            return render_template('post/render_preview.html', reload="refresh", type=5, text="Image-Processing is starting, please wait a while.", domain=current_app.config['DOMAIN'], fin=False)
        else:
            return render_template('post/render_preview.html', url=arr['file'], reload="refresh", type=5, text="Processing...", domain=current_app.config['DOMAIN'], fin=False)
