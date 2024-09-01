import flask
from flask import Blueprint, request, make_response
from flask.typing import ResponseReturnValue
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app import database, word_lists
from app.user import User, login_manager
from app.online import socketids, update_userlist

login_bp = Blueprint('login', __name__)
login_bp.login_manager = login_manager
login_bp.login_manager.login_view = "login_page"

# @bp.route('/')
# def home():
#     return render_template('login.html')

@login_bp.route("/logout")
@login_required
def logout():
    """Log out the current user"""
    User.delete_user(request.cookies.get("Userid"))
    logout_user()
    # sid = socketids[request.cookies.get("Userid")]
    del socketids[request.cookies.get("Userid")]
    # update_userlist(sid, {'status': 'offline'}, request.cookies.get("Userid"))
    resp = make_response(flask.redirect(flask.url_for("login_page")))
    resp.set_cookie("Userid", "", expires=0)
    return resp


@login_bp.route("/login", methods=["POST", "GET"])
@login_bp.route("/", methods=["GET", "POST"])
def login_page() -> ResponseReturnValue:
    """Show the login page."""
    # socketid = request.sid
    # print(current_user,'current user')
    if current_user.is_authenticated:
        # return flask.redirect(flask.url_for("chat_page"))
        print('existing user')

    if request.method == "POST":
        # redo client side checks here on server side, like signup
        username = request.form.get("username")
        password = request.form.get("password")
        TOSagree = request.form.get("TOSagree")
        socketid = request.form.get("socket")
        next_page = request.args.get("next")
        user = database.find_login_data(username, False)
        # print(userids)
        if user is None:
            return flask.render_template(
                "login.html", error="That account does not exist!"
            )
        # userid = user["userId"]
        if TOSagree != "on":
            return flask.render_template(
                "login.html", error="You did not agree to the TOS!"
            )

        if User.check_username(username, user["username"]) and User.check_password(
            user["password"], password
        ):
            user_obj = User.add_user_class(username, user, user["userId"])
            login_user(user_obj)
            socketids[user["userId"]] = socketid
            update_userlist(socketid, {"status": "active"}, user["userId"])
            if next_page is None:
                if "adminpass" in user["SPermission"]:
                    next_page = flask.url_for("chat.admin_page")
                else:
                    next_page = flask.url_for("chat.chat_page")
            else:
                if "editor" in next_page:
                    next_page = flask.url_for("projects")
                if next_page not in word_lists.approved_links:
                    next_page = flask.url_for("chat.chat_pagechat_page")
                    if "adminpass" in user["SPermission"]:
                        next_page = flask.url_for("chat.chat_pageadmin_page")
            resp = flask.make_response(flask.redirect(next_page))
            resp.set_cookie("Username", user["username"])
            resp.set_cookie("Theme", user["theme"])
            resp.set_cookie(
                "Profile",
                user["profile"] if user["profile"] != "" else "/static/favicon.ico",
            )
            resp.set_cookie("Userid", user["userId"])
            resp.set_cookie("DisplayName", user["displayName"])
            resp.set_cookie("test", "e e")
            return resp
        else:
            return flask.render_template(
                "login.html", error="That username or password is incorrect!"
            )
    else:
        return flask.render_template("login.html")#, appVersion=application.appVersion)
