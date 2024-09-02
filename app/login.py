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
login_bp.login_manager.login_view = "login.login_page"

# @bp.route('/')
# def home():
#     return render_template('login.html')

@login_bp.route("/logout")
@login_required
def logout():
    """Log out the current user"""
    uuid = request.cookies.get("Userid")
    User.delete_user(uuid)
    logout_user()
    resp = make_response(flask.redirect(flask.url_for("login_page")))
    resp.set_cookie("Userid", "", expires=0)
    user = User.get_user_by_id(uuid)
    if user and user.status != "offline-locked":
        user.status = "offline"
    database.set_offline(uuid)
    update_userlist(socketids[uuid], {"status": "offline"}, uuid)
    del socketids[uuid]
    return resp


@login_bp.route("/login", methods=["POST", "GET"])
@login_bp.route("/", methods=["GET", "POST"])
def login_page() -> ResponseReturnValue:
    """Show the login page."""
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("chat.chat_page"))

    if request.method == "POST":
        # redo client side checks here on server side, like signup
        username = request.form.get("username")
        password = request.form.get("password")
        tos_agree = request.form.get("TOSagree")
        socketid = request.form.get("socket")
        next_page = request.args.get("next")
        user = database.find_login_data(username, False)
        if user is None:
            return flask.render_template(
                "login.html", error="That account does not exist!"
            )
        if tos_agree != "on":
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
                next_page = flask.url_for("admin_page") if "adminpass" in \
                    user["SPermission"] else flask.url_for("chat_page")
            else:
                if "editor" in next_page:
                    next_page = flask.url_for("projects")
                if next_page not in word_lists.approved_links:
                    next_page = flask.url_for("chat.chat_page")
                    if "Debugpass" == user["SPermission"][0]:
                        next_page = flask.url_for("chat.dev_page")
                    if "adminpass" == user["SPermission"][0]:
                        next_page = flask.url_for("chat.admin_page")
                    if "modpass" == user["SPermission"][0]:
                        next_page = flask.url_for("chat.mod_page")
            resp = flask.make_response(flask.redirect(next_page))
            resp.set_cookie("Username", user["username"])
            resp.set_cookie("Theme", user["theme"])
            profile_image = (
                user.get("profile")
                or "/static/favicon.ico"
            )
            resp.set_cookie("Profile",profile_image)
            resp.set_cookie("Userid", user["userId"])
            resp.set_cookie("DisplayName", user["displayName"])
            return resp
        # else:
        return flask.render_template(
            "login.html", error="That username or password is incorrect!"
        )
    # else:
    return flask.render_template("login.html")#, appVersion=application.app_version)