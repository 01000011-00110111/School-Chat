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
var sudo_button = document.querySelectorAll(".sudo_cmd_button");
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
});

/**
 * This function generates command menu buttons using JavaScript 
 * @param {*} command_name 
 * @param {*} trigger 
 * @param {*} command 
 * @param {*} privilege 
 */
const create_command = (command_name, trigger, command, privilege) => {
    sudo_button = document.querySelectorAll(".sudo_cmd_button")
    let command_button, li, ul

    command_button = document.createElement('button');
    ul = document.getElementById('sudo_list');
    li = document.createElement('li');

    command_button.innerHTML = `${trigger}${command_name}`;
    command_button.setAttribute('command', command);
    command_button.setAttribute('trigger', trigger);
    command_button.setAttribute('privilege', privilege);
    command_button.classList.add('sudo_cmd_button');

    ul.appendChild(li);
    li.appendChild(command_button);
}

/**
 * Resets the sudo button count when called
 */
const reset_button_count = () => {
    sudo_button = document.querySelectorAll(".sudo_cmd_button");
}

/** 
 * This controls the button length letting js assign command_buttons and command_badges 
 */
const generate_badges = () => {
    reset_button_count();
    for (let index = 0; index < sudo_button.length; index++) {
        ul = document.getElementById("sudo_list");
        li = ul.getElementsByTagName('li');

        const command_tag = document.createElement('div');
        command_tag.classList.add('badge');
        command_tag.classList.add(`${sudo_button[index].getAttribute("privilege")}`)
        command_tag.innerHTML = sudo_button[index].getAttribute("privilege")
        li[index].appendChild(command_tag)
    };
};

/**
 * Adds a click event to all the buttons on the command list
 */
const add_command_click = () => {
    reset_button_count();
    for (let index = 0; index < sudo_button.length; index++) {
        sudo_button[index].addEventListener('click', () => {
            message.value = `${sudo_button[index].getAttribute("trigger")}${sudo_button[index].getAttribute("command")}`;
            message.focus();
            close_command_menu();
        });
    };
};

/**
 * Searches the sudo command menu
 */
function search_commands() {
    reset_button_count();
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

/**
 * This function creates a customizable disclaimer popup
 * @param {*} title 
 * @param {*} message 
 * @param {*} link 
 */
const disclaimer = (title, message, link) => {
    if (!document.getElementById("disclaimer_background")) {
        const disclaimer_backdrop = document.createElement('div');
        const disclaimer_body = document.createElement('div');
        const disclaimer_control_panel = document.createElement('div');
        const disclaimer_title = document.createElement('h2');
        const disclaimer_message = document.createElement('p');
        const back_button = document.createElement('button');
        const continue_button = document.createElement('button');

        disclaimer_title.innerHTML = title;
        disclaimer_message.innerHTML = `${message} ${link}`;
        back_button.innerHTML = "Stay here";
        continue_button.innerHTML = "Continue";

        disclaimer_backdrop.setAttribute("id", "disclaimer_background");
        disclaimer_body.classList.add("disclaimer");
        disclaimer_control_panel.classList.add("disclaimer_buttons");
        disclaimer_title.classList.add("disclaimer_title");
        continue_button.setAttribute("id", "continue_button");
        back_button.setAttribute("id", "stay_button");
        disclaimer_message.setAttribute("id", "message_body");

        document.body.appendChild(disclaimer_backdrop);
        disclaimer_backdrop.appendChild(disclaimer_body);
        disclaimer_body.appendChild(disclaimer_title);
        disclaimer_body.appendChild(disclaimer_message);
        disclaimer_body.appendChild(disclaimer_control_panel);
        disclaimer_control_panel.appendChild(back_button);
        disclaimer_control_panel.appendChild(continue_button);

        back_button.addEventListener('click', () => {
            disclaimer_backdrop.remove();
        });

        continue_button.addEventListener('click', () => {
            disclaimer_backdrop.remove();
            window.open(link, '_blank').focus();
        });
    }
}

const hyperlinks = document.querySelectorAll('a');

const isValidUrl = urlString => {
    let url;
    try {
        url = new URL(urlString);
    }
    catch(e) {
        return false;
    }
    return url.protocol === "http:" || url.protocol === "https:";
};

const default_leave_msg = "You are about to leave this site. You clicked on a link that leads you to another site. Continue at your own risk. <br> <br>";

let links = {
    "approved_links": [],
    "banned_links": []
}

let final_links = [];

const fetch_links = async () => {

    for (let index = 0; index < final_links.length; index++) {
        final_links.pop();  
    }

    for (let index = 0; index < links["approved_links"].length; index++) {
        links["approved_links"].pop();
    }

    for (let index = 0; index < links["banned_links"].length; index++) {
        links["banned_links"].pop();
    }

fetch('/static/link_data.json')
    .then((response) => response.json())
    .then((json) => {
        links.approved_links.push(json["links"][0]["approved_links"])
        links.banned_links.push(json["links"][0]["banned_links"])
        console.log(`Approved Links: ${json["links"]["approved_links"]}`);
        console.log(`Banned Links: ${json["links"]["banned_links"]}`);
        console.info("Link list has been updated");
    });
};
fetch_links();

setInterval(fetch_links, 8000);

/**
 * This function activates the hyperlinks when chat is loaded,
 * This function takes no parameters.
 */
const activate_hyperlinks = () => {
    const message_div = document.querySelectorAll(".message");

    for (let index = 0; index < links["approved_links"][0].length; index++) {
        final_links.push(links["approved_links"][0][index]);
    }

    for (let index = 0; index < links["banned_links"][0].length; index++) {
        final_links.push(links["banned_links"][0][index]); 
    }


    for (let messages = 0; messages < message_div.length; messages++) {
        const chat_hyperlinks = message_div[messages].querySelectorAll('a');

        for (let index = 0; index < chat_hyperlinks.length; index++) {
            chat_hyperlinks[index].addEventListener('click', (event) => {
                for (let approved = 0; approved < links["approved_links"][0].length; approved++) {
                    if (links["approved_links"][0][approved].includes(chat_hyperlinks[index].hostname)) {
                        document.getElementById("disclaimer_background").remove();
                    }
                }

                for (let banned = 0; banned < links["banned_links"][0].length; banned++) {
                    if (links["banned_links"][0][banned].includes(chat_hyperlinks[index].hostname)) {
                        event.preventDefault();
                        disclaimer("Link could not be opened", "We've detected that this link is a banned link therefore we did not open it", chat_hyperlinks[index]);
                        document.getElementById("continue_button").remove();
                    }
                }


                for (let loop_links = 0; loop_links < final_links.length; loop_links++) {
                    if (!final_links[loop_links].includes(chat_hyperlinks[index].hostname)) {
                        event.preventDefault();
                        disclaimer("You are leaving the School chat platform", default_leave_msg, chat_hyperlinks[index]);
                    }
                }
            });
        }
    }
};

for (let index = 0; index < hyperlinks.length; index++) {
    hyperlinks[index].addEventListener('click', (event) => {
        if (isValidUrl(hyperlinks[index].href)) {
            if (hyperlinks[index].hostname === "www6.school-chat.us" || hyperlinks[index].hostname === "localhost") {
                null
            } else {
                event.preventDefault();
                disclaimer("You are leaving the School chat platform", default_leave_msg, hyperlinks[index])
            };
        };
    });
};

/**
 * Creates a sudo command button for every user in the chat allowing you to ping them.
 */
const ping_users_command = () => {
    for (let index = 0; index < users_list.onlineList.length; index++) {
        create_command(
            users_list.onlineList[index].username,
            "@",
            users_list.onlineList[index].username,
            "user"
        );
    }

    for (let index = 0; index < users_list.offlineList.length; index++) {
        create_command(
            users_list.offlineList[index].username,
            "@",
            users_list.offlineList[index].username,
            "user"
        );
    }
};

/**
 * This function checks to see if the user is focused on the tab
 */
const checkFocus = () => {
    if (document.hasFocus()) {
        const isInStandaloneMode = () =>
            (window.matchMedia('(display-mode: standalone)').matches) || (window.navigator.standalone) || document.referrer.includes('android-app://');
      
        if (isInStandaloneMode()) {
            navigator.setAppBadge(0);
            unreadMessages = 0;
        }
    }
};
setInterval(checkFocus, 100);

window.onload = () => {
    setTimeout(activate_hyperlinks, 100);
    ping_users_command();
    add_command_click();
    generate_badges();
}