@app.route("/signup", methods=["POST"])
# @limiter.limit("1 per day")
def signup_post() -> ResponseReturnValue:
    """The creating of an account."""
    # global verification_code_list
    # global verification_code
    SUsername = request.form.get("SUsername")
    SPassword = request.form.get("SPassword")
    SPassword2 = request.form.get("SPassword2")
    SRole = request.form.get("SRole")
    SDisplayname = request.form.get("SDisplayname")
    SEmail = request.form.get("SEmail")

    result, msg = accounting.run_regex_signup(SUsername, SRole, SDisplayname)
    if result is not False:
        return flask.render_template(
            "signup-index.html",
            error=msg,
        )
    email_check = accounting.check_if_disposable_email(SEmail)
    if email_check == 2:
        return flask.render_template("signup-index.html", error="That email is banned!")
    elif email_check == 1:
        return flask.render_template(
            "signup-index.html", error="That email is not valid!"
        )
    if SPassword != SPassword2:
        return flask.render_template(
            "signup-index.html",
            error="Password boxes do not match!",
            SUsername=SUsername,
            SRole=SRole,
            SDisplayname=SDisplayname,
        )
    possible_user = database.find_account({"username": SUsername}, "vid")
    possible_dispuser = database.find_account(
        {"displayName": SDisplayname}, "customization"
    )
    # print("again")
    if (
        possible_user is not None
        or possible_dispuser is not None
        or SUsername in word_lists.banned_usernames
        or SDisplayname in word_lists.banned_usernames
    ):
        return flask.render_template(
            "signup-index.html",
            error="That Username/Display name is already taken!",
            SRole=SRole,
        )
    possible_email = database.find_account({"email": SEmail}, "vid")
    if possible_email is not None:
        return flask.render_template(
            "signup-index.html",
            error="That Email is already used!",
            SEmail=SEmail,
            SUsername=SUsername,
            SDisplayname=SDisplayname,
            SRole=SRole,
        )
    accounting.create_user(SUsername, SPassword, SEmail, SRole, SDisplayname)
    log.log_accounts(f"A user has made a account named {SUsername}")
    return flask.redirect(flask.url_for("login_page"))


@app.route("/signup", methods=["GET"])
def signup_get() -> ResponseReturnValue:
    """Serve the signup page."""
    return flask.render_template("signup-index.html")


@app.route("/verify/<userid>/<verification_code>")
def verify(userid, verification_code):
    """Verify a user."""
    user_id = database.find_account({"userId": userid}, "vid")
    if user_id is not None:
        user_code = accounting.create_verification_code(user_id)
        if user_code == verification_code:
            database.update_account_set(
                "perm", {"userId": user_id["userId"]}, {"$set": {"locked": "false"}}
            )
            user = user_id["username"]
            log.log_accounts(
                f"The account {user} is now verified and may now chat in any chat room."
            )
            return f"{user} has been verified. You may now chat in other chat rooms."
    return "Invalid verification code."