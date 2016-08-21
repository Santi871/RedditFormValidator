from flask import Flask, redirect, request, Response
from webapp import utils
import praw
import datetime

REDDIT_CLIENT_ID = utils.get_token("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = utils.get_token("REDDIT_CLIENT_SECRET")
REDIRECT_URI = utils.get_token("REDIRECT_URI")
FORM_PREFILLED_URL_TEMPLATE = utils.get_token("FORM_PREFILLED_URL_TEMPLATE", section='form')

app = Flask(__name__, static_url_path='')
r = praw.Reddit("windows:Google Form validator (access form with Reddit identity) v0.1 - by /u/Santi871")
r.set_oauth_app_info(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDIRECT_URI)


@app.route('/auth')
def oauth():
    url = r.get_authorize_url('uniqueKey')
    return redirect(url, code=302)


@app.route('/authorize_callback')
def authorized():
    code = request.args.get('code', ' ')

    try:
        r.get_access_information(code)
    except praw.errors.OAuthInvalidGrant:
        return Response(), 403

    user = r.get_me()
    name = user.name
    now = datetime.datetime.now()

    with open("authorized_users", "a+") as text_file:
        text_file.write(name + "    " + now.strftime("%Y-%m-%d %H:%M") + '\n')

    url = FORM_PREFILLED_URL_TEMPLATE + name
    return redirect(url, code=302)
