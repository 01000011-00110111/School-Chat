let prevValues = {};

function updateValues() {
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

  inputIds.forEach(id => {
    const element = document.getElementById(id);
    const currentValue = element.value;
    if (prevValues[id] !== currentValue) {
      console.log(id, "changed:", prevValues[id], "->", currentValue);
      prevValues[id] = currentValue;
    }
  });
}

// Check for changes every 500 milliseconds (0.5 seconds)
setInterval(updateValues, 500);
