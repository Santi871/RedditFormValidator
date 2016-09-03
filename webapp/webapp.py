from flask import Flask, redirect, request, Response
from webapp import utils
import praw
import datetime

REDDIT_CLIENT_ID = utils.get_token("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = utils.get_token("REDDIT_CLIENT_SECRET")
REDIRECT_URI = utils.get_token("REDIRECT_URI")

app = Flask(__name__, static_url_path='')
r = praw.Reddit("windows:Google Form validator (access form with Reddit identity) v0.2 - by /u/Santi871")
r.set_oauth_app_info(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDIRECT_URI)
ip_form_ids = dict()


@app.route('/auth')
def oauth():
    url = r.get_authorize_url('uniqueKey')
    form_id = request.args.get('form_id')
    field_id = request.args.get('field_id')
    ip_form_ids[request.remote_addr] = form_id + "," + field_id

    return redirect(url, code=302)


@app.route('/authorize_callback')
def authorized():
    code = request.args.get('code', ' ')

    try:
        split_ids = ip_form_ids[request.remote_addr].split(',')
    except KeyError:
        return "There was an error processing your request, please try again..."

    ip_form_ids.pop(request.remote_addr, None)
    form_id = split_ids[0]
    field_id = split_ids[1]

    try:
        r.get_access_information(code)
    except praw.errors.OAuthInvalidGrant:
        return Response(), 403

    user = r.get_me()
    name = user.name
    now = datetime.datetime.now()

    with open("authorized_users", "a+") as text_file:
        text_file.write(name + "    " + now.strftime("%Y-%m-%d %H:%M") + '\n')

    url = "https://docs.google.com/forms/d/e/" + form_id + "/viewform?entry." + field_id + "=" + name

    return redirect(url, code=302)
