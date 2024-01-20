// Copyright (C) 2023  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat

let prevValues = {};
const numExamples = 1; // Number of examples to create

const responses = [
    { message: "This is a test response.", rarity: 95 },
    { message: "The Devs that made this chat are cserver, and cseven.", rarity: 80 },
    { message: "The chat is always changing and improving so get ready for the next new change.", rarity: 80 },
    { message: "This is a chat app, what else did you think this is?", rarity: 80 },
    { message: "Try changing your user and role colors for a more fun experience.", rarity: 70 },
    { message: "Try $sudo help in chat to find out all the command you can use.", rarity: 60 },
    { message: "Never gonna give you up, never gonna let you down.", rarity: 45 },
    { message: "This is how the chat was made https://stackoverflow.com.", rarity: 5 },
    { message: "Challenge if you can the rarest message on 4 messages and show proof to a dev then you rainbow role colors!(This challenge is over new one soon)", rarity: 2 },
    { message: "Try $sudo E in chat.", rarity: 1 },
];

function pickRandom(rarities) {
    // Calculate the sum of all rarities
    var totalRarity = rarities.reduce((sum, response) => sum + response.rarity, 0);
    
    if (totalRarity <= 0) {
        return;
    }
    
    // Create an array of totalRarity elements, based on the rarity field
    var probability = rarities.flatMap(response => Array(response.rarity).fill(response.message));
    
    // Pick one
    var pIndex = Math.floor(Math.random() * totalRarity);
    return probability[pIndex];
}

function createExamples() {
    const exampleContainer = document.getElementById("example");

    if (!exampleContainer) {
        return;
    }

    // Clear existing examples (if any)
    exampleContainer.innerHTML = ""; 
    for (let i = 1; i <= numExamples; i++) {
        const exampleId = `example${i}`;
        const exampleElement = document.createElement("div");
        exampleElement.setAttribute("id", exampleId);
        exampleContainer.appendChild(exampleElement);
    }
}

function updateExamples() {
    const inputIds = [
        "user",
        "username",
        "role",
        "message_color",
        "role_color",
        "user_color",
        "Apassword",
        "profile"
    ];
    
    const exampleContainer = document.getElementById("example");
    if (!exampleContainer) {
        return;
    }

    let profile = document.getElementById("profile").value;
    if (profile === '') {profile = 'static/favicon.ico'}
    const userColor = document.getElementById("user_color").value;
    const username = document.getElementById("username").value;
    const roleColor = document.getElementById("role_color").value;
    const role = document.getElementById("role").value;
    const messageColor = document.getElementById("message_color").value;

    inputIds.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            const currentValue = element.value;
            if (prevValues[id] !== currentValue) {
                prevValues[id] = currentValue;
                for (let i = 1; i <= numExamples; i++) {
                    const exampleId = `example${i}`;
                    const exampleElement = document.getElementById(exampleId);
                    if (exampleElement) {
                        const randomResponse = pickRandom(responses);
                        exampleElement.innerHTML = `[Mon 8:00 PM] <input type="image" class='pfp' src='${profile}'> <font color="${userColor}">${username}</font> (<font color="${roleColor}">${role}</font>) - <font color="${messageColor}">${randomResponse}</font>`;
                    }
                }
            }
        }
    });
}

// Create examples when the page loads

createExamples();

// Update examples every 250 milliseconds (0.25 seconds)
setInterval(updateExamples, 250);
socket.emit("username", getCookie("Username"), 'settings');


socket.on("force_username", (_statement) => {
    socket.emit("username", getCookie("Username"), 'settings');
});

const holidays = {
  "halloween": {
    name: "halloween",
    start: "10-01",
    end: "10-31"
  },
};

function setTheme(theme) {
  let currentDate = new Date();
  let month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
  let day = currentDate.getDate().toString().padStart(2, '0');
  var themeBtn = document.querySelector(".themeBtn");
  var themeDropdown = document.querySelector(".themeContent");

  for (const key in holidays) {
    const holiday = holidays[key];
    if (`${month}-${day}` >= holiday.start && `${month}-${day}` <= holiday.end && theme === 'holiday') {
      theme = holiday.name;
      break;
    }
  }

  console.log(theme);

  themeBtn.innerText = "You picked: " + capitalizeFirstLetter(theme);
  document.getElementsByName("theme")[0].value = theme;
  themeDropdown.style.display = "none";
}

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function openTab(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
  }
  
  // Opens the defualt tab
  openTab(event, "My-Profile")