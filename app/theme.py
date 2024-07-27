@app.route("/editor")
@login_required
def editor():
    return flask.render_template("theme/editor.html")


@app.route("/projects")
@login_required
def projects():
    return flask.render_template("theme/projects.html")


@socketio.on("get_projects")
def handle_project_requests():
    socketid = request.sid
    userid = request.cookies.get("Userid")
    displayname = request.cookies.get("DisplayName").replace('"', "")
    projects = database.get_projects(userid, displayname)
    projects_fixed = []
    # print(projects)
    for project in projects:
        del project["_id"]
        del project['theme']
        # if "author" in project and len(project["author"]) > 1:
        project["author"] = project["author"][1:]
        projects_fixed.append(project)
    # print(projects_fixed)
    emit("projects", (projects_fixed), to=socketid)


@socketio.on("create_project")
def handle_projecet_creation():
    socketid = request.sid
    userid = request.cookies.get("Userid")
    user = User.get_user_by_id(userid)
    if user.themeCount >= 3:
        emit("response", ("You have hit your project limit", True), to=socketid)
        return
    print(user.themeCount)
    # displayname = request.cookies.get('DisplayName').replace('"', '')
    while True:
        code = ""
        for _ in range(5):
            code += random.choice(ascii_uppercase)

        if code not in database.get_all_projects():
            break
    project = database.create_project(userid, user.displayName, code)
    user.themeCount += 1
    del project["_id"]
    project['theme'] = {}
    project["author"] = project["author"][1:]
    emit("set_theme", project, to=socketid)


@socketio.on("get_project")
def send_project(theme_id):
    socketid = request.sid
    project = database.get_project(theme_id)
    del project["_id"]
    project['theme'] = {}
    # if "author" in project and len(project["author"]) > 1:
    project["author"] = project["author"][1:]
    emit("set_theme", project, to=socketid)


@socketio.on("save_project")
def handle_save_project(themeID, theme, name, publish):
    socketid = request.sid
    database.save_project(themeID, theme, name, publish)
    message = 'Project Published' if publish else 'Project Saved'
    emit("response", (message, False), to=socketid)
    

@socketio.on("update_theme_status")
def handel_status_change(themeID, status):
    database.update_theme_status(themeID, status)


@socketio.on("delete_project")
def handle_delete_project(project):
    socketid = request.sid
    user = User.get_user_by_id(request.cookies.get("Userid"))
    user.themeCount -= 1
    database.delete_project(project)
    emit("response", ("Project deleted", False), to=socketid)


@socketio.on("get_themes")
def handle_theme_requests():
    socketid = request.sid
    uuid = request.cookies.get("Userid")
    themes = database.get_all_projects()
    themes_fixed = []
    # print(list(projects))
    for theme in themes:
        if theme['theme'] == {}:
            continue
        if theme["status"] == "private" and theme['author'][0] != uuid:
            continue
        if theme['name'] == 'Untitled Project':
            continue
        del theme["_id"]
        if 'project' in theme:
            del theme['project']
        del theme["status"]
        del theme["theme"]
        # if "author" in project and len(project["author"]) > 1:
        theme["author"] = theme["author"][1:]
        themes_fixed.append(theme)
    # print(projects_fixed)
    emit("receve_themes", (themes_fixed), to=socketid)


@socketio.on("get_theme")
def send_theme(theme_id):
    socketid = request.sid
    theme = database.get_project(theme_id)
    # print(theme)
    if theme is None:
        theme = database.get_project("dark")
    del theme["_id"]
    if 'project' in theme:
        del theme['project']
    theme["author"] = theme["author"][1:]
    # del project['themeID']
    del theme["status"]
    # del project['name']
    # print(theme)
    emit("set_theme", theme, to=socketid)