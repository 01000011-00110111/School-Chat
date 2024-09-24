// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
const clearSearchButton = document.getElementById("clearSearchButton");
const searchInput = document.getElementById("searchInput");
const ellipsis_button = document.getElementById("ellipsis_button");
const ellipsis_dropdown = document.getElementById("ellipsis_dropdown");
const logout_button = document.getElementById("logout_button");
const back_button = document.getElementById("back_button");

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
    clearSearchButton.classList.remove("hidden");
  }
  else
  {
    clearSearchButton.classList.add("hidden");
  }
}
setInterval(showclearButton, 100)

function Runstartup() {
  socket.emit('get_projects');
};

// socket.on("projects", (projects_list) => {
//   console.log(projects_list)
//   const projectsList = document.getElementById("ProjectList");
//   for (let i = 0; i < projects_list.length; i++) {
//     const newProject = document.createElement("button");
//     newProject.innerHTML = `${projects_list[i].author}'s | ${projects_list[i].name}`
//     newProject.setAttribute("onclick", `set_theme('${projects_list[i].themeID}');`)
//     newProject.classList.add("project_panel")
//     projectsList.appendChild(newProject)
//   }

//   const projectNumber = document.getElementById("projectNumber");
//   const project_panels = document.getElementsByClassName("project_panel");
//   projectNumber.innerHTML = `Workspace Projects: [${project_panels.length}]`
// });

socket.on("projects", (projects_list) => {
  console.log(projects_list);
  const projectsList = document.getElementById("ProjectList");
  // projectsList = ''

  for (let i = 0; i < projects_list.length; i++) {
    const newProjectContainer = document.createElement("div");
    newProjectContainer.classList.add("project_panel_container");
    newProjectContainer.setAttribute("data-id", projects_list[i].themeID);

    const projectButton = document.createElement("button");
    projectButton.innerHTML = `${projects_list[i].author}'s | ${projects_list[i].name} | Status: ${capitalize(projects_list[i].status)}`;
    projectButton.setAttribute("onclick", `set_theme('${projects_list[i].themeID}');`);
    projectButton.classList.add("project_panel");
    newProjectContainer.appendChild(projectButton);

    const dropdown = document.createElement("div");
    dropdown.classList.add("dropdown");

    const dropdownButton = document.createElement("button");
    dropdownButton.innerHTML = `<i class="fa-solid fa-ellipsis-vertical"></i>`;
    dropdownButton.classList.add("dropdown_button");
    dropdown.appendChild(dropdownButton);

    const dropdownContent = document.createElement("div");
    dropdownContent.classList.add("dropdown_content");

    const option1 = document.createElement("a");
    let view = projects_list[i].status === 'private' ? 'public' : 'private';
    option1.innerHTML = `<i class="fa-regular fa-eye"></i> Set to ${capitalize(view)}`;
    option1.setAttribute("onclick", `update_status('${projects_list[i].themeID}', '${projects_list[i].status}');`);
    dropdownContent.appendChild(option1);

    const option2 = document.createElement("a");
    option2.innerHTML = `<i class="fa-solid fa-trash" style="color: #ff2600;"></i> Delete`;
    option2.setAttribute("onclick", `delete_project('${projects_list[i].themeID}');`);
    dropdownContent.appendChild(option2);

    dropdown.appendChild(dropdownContent);
    newProjectContainer.appendChild(dropdown);

    projectsList.appendChild(newProjectContainer);
  }

  const projectNumber = document.getElementById("projectNumber");
  const project_panels = document.getElementsByClassName("project_panel_container");
  projectNumber.innerHTML = `Workspace Projects: [${project_panels.length}]`;
});


function new_project() {
  sessionStorage.setItem('editing', '');
  ToPage('/editor');
}


function set_theme(theme) {
  sessionStorage.setItem('editing', theme);
  ToPage('/editor');
}

function capitalize(string) {
  if (string.length === 0) return string;
  return string.charAt(0).toUpperCase() + string.slice(1);
}


function update_status(themeID, currentStatus) {
  let newStatus = currentStatus === 'private' ? 'public' : 'private';
  socket.emit('update_theme_status', themeID, newStatus);

  // Update the main project button text
  const buttonToUpdate = document.querySelector(`[data-id="${themeID}"] button.project_panel`);
  // if (buttonToUpdate) {
    const currentText = buttonToUpdate.innerHTML;
    const newText = currentText.replace(`Status: ${capitalize(currentStatus)}`, `Status: ${capitalize(newStatus)}`);
    buttonToUpdate.innerHTML = newText;
  // }

  // Update the dropdown option text
  const optionToUpdate = document.querySelector(`[onclick="update_status('${themeID}', '${currentStatus}');"]`);
  if (optionToUpdate) {
    optionToUpdate.innerHTML = `<i class="fa-regular fa-eye"></i> Set to ${capitalize(currentStatus)}`;
    optionToUpdate.setAttribute("onclick", `update_status('${themeID}', '${newStatus}');`);
  }
}



function delete_project(themeID) {
  if (confirm("Are you sure you want to delete this Theme?")) {
    socket.emit('delete_project', themeID);
    deleteProject(themeID);
    updateProjectCount();
    alert("Theme deleted!");
  }
}

function deleteProject(id) {
  const projectContainer = document.querySelector(`.project_panel_container[data-id='${id}']`);
  if (projectContainer) {
    projectContainer.remove();
    updateProjectCount();
  }
}

function updateProjectCount() {
  const projectNumber = document.getElementById("projectNumber");
  const project_panels = document.getElementsByClassName("project_panel_container");
  projectNumber.innerHTML = `Workspace Projects: [${project_panels.length}]`;
}

const import_input = document.getElementById('import_theme_input')
import_input.addEventListener('input', () => {
  new_project()
})

// socket.on('response', (response) => {
//   console.log(response)
//   document.getElementById('response_text').innerHTML = response
// });

ellipsis_button.addEventListener('click', (event) => {
  if (ellipsis_dropdown.style.display != "grid") {
    ellipsis_dropdown.style.display = "grid";
  } else {
    ellipsis_dropdown.style.display = "none";
  }
});

logout_button.addEventListener('click', (event) => {
  window.location.href = "/logout";
});

back_button.addEventListener('click', (event) => {
  window.location.href = ".";
});