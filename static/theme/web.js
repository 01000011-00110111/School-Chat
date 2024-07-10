const clearSearchButton = document.getElementById("clearSearchButton");
const searchInput = document.getElementById("searchInput");

function ToPage(URL) {
  window.location.href = URL;
}

function OpenExternalPage(External_Url) {
  window.open(External_Url, "_blank");
}

clearSearchButton.addEventListener('click', () => {
  searchInput.value = "";
});

const showclearButton = () => {
  if (searchInput.value != '') {
    clearSearchButton.classList.remove("hidden")
  }
  else
  {
    clearSearchButton.classList.add("hidden")
  }
}
setInterval(showclearButton, 100)

function Runstartup() {
  socket.emit('get_projects')
}

socket.on("projects", (projects_list) => {
  console.log(projects_list)
  const projectsList = document.getElementById("ProjectList");
  for (let i = 0; i < projects_list.length; i++) {
    const newProject = document.createElement("button");
    newProject.innerHTML = `${projects_list[i].author}'s | ${projects_list[i].name}`
    newProject.setAttribute("onclick", `set_theme('${projects_list[i].name}');`)
    newProject.classList.add("project_panel")
    projectsList.appendChild(newProject)
  }

  const projectNumber = document.getElementById("projectNumber");
  const project_panels = document.getElementsByClassName("project_panel");
  projectNumber.innerHTML = `Workspace Projects: [${project_panels.length}]`
});

function new_project() {
  sessionStorage.setItem('editing', '');
  ToPage('/editor')
}


function set_theme(theme) {
  sessionStorage.setItem('editing', theme);
  ToPage('/editor')
}