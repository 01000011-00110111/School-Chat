function update() {
    let user = document.getElementById("user")["value"];
    let displayname = document.getElementById("username")["value"];
    let role = document.getElementById("role")["value"];
    let Cmessage = document.getElementById("message_color")["value"];
    let Crole = document.getElementById("role_color")["value"];
    let Cuser = document.getElementById("user_color")["value"];
    let passwd = document.getElementById("Apassword")["value"];
    let profile = document.getElementById("profile")["value"];
    
    socket.emit('update_acc', displayname, role, messageC, roleC, userC, passwd, user, profile);
}