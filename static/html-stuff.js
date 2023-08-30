// Copyright (C) 2023  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat

function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

function toggleDropdown() {
    let themeDropdown = document.querySelector(".themeContent");
    if (themeDropdown.style.display === "block") {
        themeDropdown.style.display = "none";
    } else {
        themeDropdown.style.display = "block";
    }
}

// pfp button

function OpenAC() {
    let AC = document.getElementById("AccControls");
    if (AC.style.display === "grid") {
        AC.style.display = "none";
    } else {
        AC.style.display = "grid";
    }
}

function OpenTOS() {
  let TOSPopup = document.getElementById("tos-popup");
  TOSPopup.style.display = "grid";
}

function CloseTOS() {
  let TOSPopup = document.getElementById("tos-popup");

  TOSPopup.style.display = "none";
}