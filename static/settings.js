let prevValues = {};

const responses = [
  { message: "This is a test response", rarity: 20 },
  { message: "Try changing your user and role colors for a more fun experience", rarity: 15 },
  { message: "Response 3", rarity: 25 },
  { message: "Response 4", rarity: 10 },
  { message: "rsponse 5", rarity: 30 },
  { message: "Try $sudo E in chat", rarity: 1 },
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
  const numExamples = 4; // Number of examples to create
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

  inputIds.forEach(id => {
    const element = document.getElementById(id);
    if (element) {
      const currentValue = element.value;
      if (prevValues[id] !== currentValue) {
        prevValues[id] = currentValue;
        for (let i = 1; i <= 4; i++) {
          const exampleId = `example${i}`;
          const exampleElement = document.getElementById(exampleId);
          if (exampleElement) {
            const randomResponse = pickRandom(responses);
            exampleElement.innerHTML = `[Mon 8:00 PM] <input type="image" class='pfp' src='${document.getElementById("profile").value}'> <font color="${document.getElementById("user_color").value}">${document.getElementById("username").value}</font> (<font color="${document.getElementById("role_color").value}">${document.getElementById("role").value}</font>) - <font color="${document.getElementById("message_color").value}">${randomResponse}</font>`;
          }
        }
      }
    }
  });
}

// Create examples when the page loads
createExamples();

// Update examples every 500 milliseconds (0.5 seconds)
setInterval(updateExamples, 500);
