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