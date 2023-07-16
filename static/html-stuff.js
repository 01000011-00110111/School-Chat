function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

function dropdownTheme() {
    document.getElementById("myDropdown").classList.toggle("show");
}

window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    } else if (!event.target.matches('.mySidenav')) {
        // what is this
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