@app.route("/settings", methods=["GET"])
@login_required
def settings_page() -> ResponseReturnValue:
    """Serve the settings page for the user."""
    user = database.find_login_data(request.cookies.get("Userid"), True)
    if request.cookies.get("Userid") != user["userId"]:
        # someone is trying something funny
        return flask.Response(
            "Something funny happened. Try Again (Unauthorized)", status=401
        )

    return flask.render_template(
        "settings.html",
        user=user["username"],
        passwd="we are not adding password editing just yet",
        email=user["email"],
        displayName=user["displayName"],
        role=user["role"],
        user_color=user["userColor"],
        role_color=user["roleColor"],
        message_color=user["messageColor"],
        profile=user["profile"],
        theme=user["theme"],
    )


@app.route("/settings", methods=["POST"])
@login_required
def customize_accounts() -> ResponseReturnValue:
    """Customize the account."""
    username = request.form.get("user")
    userid = request.cookies.get("Userid")
    displayname = request.form.get("display")
    role = request.form.get("role")
    messageC = request.form.get("message_color")
    roleC = request.form.get("role_color")
    userC = request.form.get("user_color")
    email = request.form.get("email")
    file = request.files.get("profile")  # if 'profile' in request.files else None
    theme = request.form.get("theme")
    # print(theme)
    user = User.get_user_by_id(userid)
    user_email = database.get_email(user.uuid)
    return_list = {
        "user": username,
        "passwd": "we are not adding password editing just yet",
        "displayName": displayname,
        "role": role,
        "user_color": userC,
        "role_color": roleC,
        "message_color": messageC,
        "profile": file,
        "theme": theme,
        "email": email,
    }
    # print(theme)
    old_path = user.profile
    # print(file)
    profile_location = (
        uploading.upload_file(file, old_path) if file is not None else old_path
    )

    if theme is None:
        return flask.render_template(
            "settings.html", error="Pick a theme before updating!", **return_list
        )

    theme = user.theme if theme == "" else theme
    result, error = accounting.run_regex_signup(username, role, displayname)
    if result is not False:
        return flask.render_template("settings.html", error=error, **return_list)

    if (
        database.find_account({"displayName": displayname}, "customization") is not None
        and user.displayName != displayname
    ) and displayname in word_lists.banned_usernames:
        return flask.render_template(
            "settings.html", error="That Display name is already taken!", **return_list
        )
    email_check = database.find_account({"email": email}, "vid")
    if email_check is None and user_email != email:
        verification_code = accounting.create_verification_code(user)
        accounting.send_verification_email(
            user.username, email, verification_code, user.uuid
        )
    elif email_check is not None and user_email != email:
        return flask.render_template(
            "settings.html", error="that email is taken", **return_list
        )

    if user.locked != "locked":
        database.update_account(
            user.uuid,
            messageC,
            roleC,
            userC,
            displayname,
            role,
            profile_location,
            theme,
            email,
        )
        user.update_account(
            messageC, roleC, userC, displayname, role, profile_location, theme
        )

        resp = flask.make_response(flask.redirect(flask.url_for("chat_page")))
        resp.set_cookie("Username", user.username)
        resp.set_cookie("Theme", theme)
        resp.set_cookie("Profile", profile_location)
        resp.set_cookie("Userid", user.uuid)
        error = "Updated account!"
        return resp
    else:
        if user_email == email:
            return flask.render_template(
                "settings.html",
                error="You must verify your account before you can change settings",
                **return_list,
            )
        database.update_account_set(
            "vid", {"username": username}, {"$set": {"email": email}}
        )
        error = "Updated email!"
    log.log_accounts(f"The account {user} has updated some setting(s)")
    return flask.render_template("settings.html", error=error, **return_list)


@app.route("/change-password", methods=["POST", "GET"])
def change_password() -> ResponseReturnValue:
    """Handles the user password reset request and sends the reset email."""
    if request.method == "GET":
        return flask.render_template("password_part1.html")

    if request.method == "POST":
        username = request.form.get("username")
        user = database.find_login_data(username, False)
        if user:
            accounting.password(user)
        return "check the email you used to make the account for a password reset link"
        # return flask.render_template("password_part1.html")


@app.route("/reset/<userid>/<verification_code>", methods=["POST", "GET"])
def reset_password(userid, verification_code) -> ResponseReturnValue:
    """Handles the user password reset request and sends the reset email."""
    user_id = database.find_account({"userId": userid}, "vid")
    if request.method == "GET":
        return flask.render_template(
            "password_part2.html", username=user_id["username"]
        )

    if request.method == "POST":
        password = request.form.get("password")
        password2 = request.form.get("password2")
        if user_id is not None:
            user_code = accounting.create_verification_code(user_id)

            if user_code == verification_code:
                if password != password2:
                    return flask.render_template(
                        "password_part2.html",
                        error="Your passwords do not match!",
                        username=user_id["username"],
                    )

                password_hash = hashlib.sha384(bytes(password, "utf-8")).hexdigest()

                if password_hash == user_id["password"]:
                    return flask.render_template(
                        "password_part2.html",
                        error="You can not use your previous password!",
                        username=user_id["username"],
                    )

                database.update_account_set(
                    "vid",
                    {"userId": user_id["userId"]},
                    {"$set": {"password": password_hash}},
                )
                return flask.redirect(flask.url_for("login_page"))
    return "Invalid reset code."