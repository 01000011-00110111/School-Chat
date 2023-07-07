function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

function devopenNav() {
    document.getElementById("DevStuff").style.width = "550px";
    document.getElementById("DevStuff").style.paddingLeft = "5%";
}

function devcloseNav() {
    document.getElementById("DevStuff").style.width = "0";
    document.getElementById("DevStuff").style.paddingLeft = "0";
}

function opendevchat() {
    document.getElementById("dev_chat").style.width = "1250px";
    document.getElementById("dev_chat").style.paddingLeft = "5%";
}

function closedevchat() {
    document.getElementById("dev_chat").style.width = "0";
    document.getElementById("dev_chat").style.paddingLeft = "0";
}

function ModopenNav() {

    document.getElementById("ModStuff").style.width = "550px";
    document.getElementById("ModStuff").style.paddingLeft = "5%";
}

function ModcloseNav() {
    document.getElementById("ModStuff").style.width = "0";
    document.getElementById("ModStuff").style.paddingLeft = "0";
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

function DropdownTXTtheme() {
    document.getElementById("DropdownTXT").classList.toggle("showTXT");
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