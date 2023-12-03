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

//Do not remove
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