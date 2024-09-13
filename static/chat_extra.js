socket.on("chat_muted", () => {
    const send_button = document.getElementById("send");

    message.disabled = true;
    message.placeholder = "You can't chat in this room";
    send_button.disabled = true;
})

socket.on("chat_unmuted", () => {
    const send_button = document.getElementById("send");

    message.disabled = false;
    message.placeholder = "type your message here";
    send_button.disabled = false;
})

socket.on("troll", (message, ID) => {
    renderChat(message, ID);
    var audio = new Audio('static/airhorn_default.wav');
    audio.play();
});

socket.on("pingTime", (time, ID) => {
    socket.emit('pingtest', time, ID);
});

const sudo_cmd_menu = document.getElementById("sudo_cmd_menu")

/**
 * Opens the sudo command menu and other text functions
 */
const open_command_menu = () => {
    sudo_cmd_menu.style.setProperty("display", "grid")
}

/**
 * Closes the sudo command menu and other text functions
 */
const close_command_menu = () => {
    sudo_cmd_menu.style.setProperty("display", "none")
}

/* This tirgger the sudo command menu when you type the trigger word ($, @ ,&, &*) */
const sudo_button = document.querySelectorAll(".sudo_cmd_button")
message.addEventListener('input', (event) => {
    // const inputValue = message.value.trim();
    const commandPrefixes = ["$", "@", "&", "&*", "filter:"];

    let containsCommand = commandPrefixes.some(prefix => message.value.includes(prefix));

    if (containsCommand) {
        open_command_menu();
    } else {
        close_command_menu();
    }
});

/* This closes the sudo command menu when you click the enter button */
message.addEventListener('keypress', (event) => {
    if (event.key === "Enter") {
        close_command_menu()
    }
})

/* This closes the sudo command menu when you click outside of the textinput */
message.addEventListener('focusout', (event) => {
    setTimeout(close_command_menu, 100)
})

/* This controls the button length letting js assign command_buttons and command_badges */
for (let index = 0; index < sudo_button.length; index++) {
    ul = document.getElementById("sudo_list");
    li = ul.getElementsByTagName('li');

    const command_tag = document.createElement('div');
    command_tag.classList.add(`${sudo_button[index].getAttribute("privilege")}`)
    command_tag.innerHTML = sudo_button[index].getAttribute("privilege")
    li[index].appendChild(command_tag)

    sudo_button[index].addEventListener('click', () => {
        message.value = `${sudo_button[index].getAttribute("trigger")}${sudo_button[index].getAttribute("command")}`;
        message.focus()
        close_command_menu()
    })
}

function search_commands() {
    // Declare variables
    var filter, ul, li, a, i, txtValue;
    filter = message.value.toLowerCase();
    ul = document.getElementById("sudo_list");
    li = ul.getElementsByTagName('li');
  
    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
      a = li[i].getElementsByTagName("button")[0];
      txtValue = a.textContent || a.innerText;
      if (txtValue.toLowerCase().indexOf(filter) > -1) {
        li[i].style.display = "";
      } else {
        li[i].style.display = "none";
      } if (message.value === "&*") {
        li[i].style.display = "";
      } if (message.value === `$filter{type:${sudo_button[i].getAttribute("privilege")}}`) {
        const command_badge = document.querySelectorAll(".user")
        for (let index = 0; index < command_badge.length; index++) {
            if (command_badge[index].innerHTML === "user") {
                li[i].style.display = "";
            }
        }
      } if (message.value === "color_change") {
        message.style.setProperty('animation', 'clr_typing 3s infinite')
      }
    }
}