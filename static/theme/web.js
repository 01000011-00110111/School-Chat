function ToPage(URL) {
  window.location.href = URL;
}

function OpenExternalPage(External_Url) {
  window.open(External_Url, "_blank");
}

function Runstartup() {
  socket.emit('get_projects')
}

socket.on("projects", (projects_list) => {
  const projectsList = document.getElementById("ProjectList");
  for (let i = 0; i < projects_list.length; i++) {
    const newProject = document.createElement("button");
    projectDiv.innerHTML = projects_list[i].Name
    newProject.setAttribute("onclick", "set_theme();")
    projectsList.appendChild(newProject)
  }
});


function set_theme(theme) {
  window.sessionStorage.set('editing', theme)
}