// Copyright (C) 2023  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat

function openNav() {
  if (window.screen.width <= 450) {
    document.getElementById("mySidenav").style.width = "100%";
  } else {
    document.getElementById("mySidenav").style.width = "250px";
  }
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

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function openThemes() {
  document.getElementById("themes-dropdown-content").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.themes-dropdown-button')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

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
  TOSPopup.style.display = "flex";
}

function CloseTOS() {
  let TOSPopup = document.getElementById("tos-popup");

  TOSPopup.style.display = "none";
}

// bottomButton = document.getElementById("chat-bottom-button");
// setInterval(bottom_of_chat, 1000)

// function bottom_of_chat() {
//   if (Math.floor(window.scrollY) !=+ window.scrollMaxY) {
//       bottomButton.style.display = "inline";
//   }
//   else if (Math.floor(window.scrollY) ==+ window.scrollMaxY)
//   {
//       bottomButton.style.display = "none";
//   }
// }

//Code broken as far as I know
function Prepare() {
  let ActiveNav = document.getElementById("activenav");
  let Chat = document.getElementById("chat");
  Chat.addEventListener("touchstart", startTouch, false);
  Chat.addEventListener("touchmove", moveTouch, false);
}
// Swipe Up / Down / Left / Right
var initialX = null;
var initialY = null;
 
function startTouch(e) {
  initialX = e.touches[0].clientX;
  initialY = e.touches[0].clientY;
};
 
function moveTouch(e) {
  if (initialX === null) {
    return;
  }
 
  if (initialY === null) {
    return;
  }
 
  var currentX = e.touches[0].clientX;
  var currentY = e.touches[0].clientY;
 
  var diffX = initialX - currentX;
  var diffY = initialY - currentY;
 
  if (Math.abs(diffX) > Math.abs(diffY)) {
    // sliding horizontally
    if (diffX > 0) {
      // swiped left
      ActiveNav.style.marginLeft = "61%";
    } else {
      // swiped right
      console.log("swiped right");
    }  
  } else {
    // sliding vertically
    if (diffY > 0) {
      // swiped up
      
    } else {
      // swiped down
      
    }  
  }
 
  initialX = null;
  initialY = null;
   
  e.preventDefault();
};