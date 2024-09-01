// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat

const fileInput = document.getElementById('profile');
const PfPdisplay = document.getElementById('PfPdisplay');

let prevValues = {};
const numExamples = 1; // Number of examples to create

const responses = [
    { message: "This is a test response.", rarity: 90 },
    { message: "Stay positive and have fun!", rarity: 90 },
    { message: "Welcome to the chat! Enjoy your stay, if you can.", rarity: 90 },
    { message: "Remember to be respectful to others, but not me.", rarity: 85 },
    { message: "Remember to take breaks and stay hydrated!", rarity: 85 },
    { message: "The Devs that made this chat are cserver, and cseven.", rarity: 80 },
    { message: "Got feedback? We'd love to hear it.", rarity: 80 },
    { message: "The chat is always changing and improving so get ready for the next new change.", rarity: 80 },
    { message: "This is a chat app, what else did you think this is?", rarity: 80 },
    { message: "Did you know? You can customize your chat nickname in settings, but your real nickname wont leave.", rarity: 75 },
    { message: "Try changing your user and role colors for a more fun experience.", rarity: 70 },
    { message: "Explore or make different chat themes to personalize your experience!", rarity: 70 },
    { message: "Did you know? You can use emojis in your messages to express yourself!", rarity: 65 },
    { message: "Try $sudo help in chat to find out all the command you can use.", rarity: 60 },
    { message: "Did you know you can make a theme, well only if your username doesnt start with a ¿.", rarity: 60 },
    { message: "Learn new chat commands to enhance your chatting experience.", rarity: 60 },
    { message: "Keep an eye out for special holiday themes and events!", rarity: 55 },
    { message: "Invite your friends to join the chat! if you got any.", rarity: 55 },
    { message: "Feel free to ask for help if you need it, but your better off not trying.", rarity: 50 },
    { message: "Never gonna give you up, never gonna let you down.", rarity: 45 },
    { message: "How do you organize a space party? You planet.", rarity: 45 },
    { message: "I told my computer I needed a break, and now it won’t stop sending me to the beach.", rarity: 45 },
    { message: "Why did the chicken go to the seance? To talk to the other side.", rarity: 40 },
    { message: "I used to play piano by ear, but now I use my hands.", rarity: 35 },
    { message: "Did you know if you do $sudo help it will help you.", rarity: 30 },
    { message: "Keep your chat history clean by deleting old messages. Oh wait you can't too bad.", rarity: 25 },
    { message: "Curious? Get a random fact to learn something new!", rarity: 10 },
    { message: "This is how the chat was made https://stackoverflow.com.", rarity: 5 },
    { message: "Fun fact: This chat was built using cutting-edge technology! Okay sorry I lied.", rarity: 3 },
    { message: "Parallel lines have so much in common. It’s a shame they’ll never meet.", rarity: 3 },
    { message: "Guess what? The next big feature drop is just around the corner!", rarity: 2 },
    { message: "Did you hear? Typing 'wizard' grants you magical chat powers.", rarity: 2 },
    { message: "Try $sudo E in chat.", rarity: 1 },
    { message: "Feeling lucky? Enter the lottery and see what you get!", rarity: 1 },
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
        "profile"
    ];
    
    const exampleContainer = document.getElementById("example");
    if (!exampleContainer) {
        return;
    }

    let profile = document.getElementById("PfPdisplay").src
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
socket.emit("get_theme", getCookie('Theme'));
socket.emit("get_themes");
// console.log(getCookie('Theme'))

socket.on('set_theme', (theme) => {
  console.log(theme)
  setTheme(theme['themeID'], theme['name'], theme['author'])
})

// const holidays = {
//   "halloween": {
//     name: "halloween",
//     start: "10-01",
//     end: "10-31"
//   },
// };

function setTheme(theme, name, author) {
  var themeAuthor = document.getElementById("info_theme_author")
  var selector = document.getElementById("theme-selector")
  var info_theme_text = document.getElementById("info_theme_name")
  selector.value = theme
  themeAuthor.innerHTML = author
  info_theme_text.innerHTML = `Applied theme: ${name}`
}


socket.on('receive_themes', (themes) => {
  const contentList = document.getElementById("themes_panel")
  // console.log(themes)
  for (const theme of themes) {
      const themeButton = document.createElement('a');
      themeButton.innerHTML = `<i class="fa-regular fa-file-lines" style="color: #ffffff;"></i> ${theme['name']}`;
      themeButton.setAttribute("onclick", `setTheme('${theme['themeID']}', '${theme['name']}','${theme['author']}')`)
      contentList.appendChild(themeButton);
  }
});

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

fileInput.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            PfPdisplay.src = e.target.result;
        };

        reader.readAsDataURL(file);
    }
    this.files = this.files
});

  // Opens the defualt tab
  openTab(event, "My-Profile");

  function enableNotifications() {
    // Checks if the user's browser supports notifications
    if (!"Notification" in window) {
      
      alert("Your browser does not support desktop notifications.");
  
      // It checks if the user already has notifications enabled for this site
    } else if (Notification.permission === "granted") {
      
      const notification = new Notification("Notifications Enabled");
  
      // If user has notifications disbaled then it asks for permission to enable them
    } else if (Notification.permission !== "denied") {
      
      Notification.requestPermission().then((permission) => {  
        if (permission === "granted") {
          
          const notification = new Notification("Notifications Enabled");
          
        }
      });
    }
  }