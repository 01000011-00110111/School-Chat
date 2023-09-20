document.addEventListener('DOMContentLoaded', function() {
// Constants
const SCREEN_WIDTH = 800;
const SCREEN_HEIGHT = 600;
const WALL_COLOR = "#333";
const PLAYER_COLOR = "#00F";
const ENEMY_COLOR = "#F00";
const GOAL_COLOR = "#0F0"; // Color for the goal

// Initialize canvas
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

socket.on("force_username", (_statement, ignore_user) => {
    if (getCookie('Userid') != ignore_user){
        socket.emit("username", getCookie("Username"), 'games');
    } else {socket.emit("username", 'pass', 'games');}
});

// Player
const player = {
    x: 50,
    y: 50,
    width: 32,
    height: 32,
    speed: 5,
    hp: 100,
    attacking: false,
    lastHitTime: 0, // Track the last time the player was hit
    knockback: 20, // Knockback distance
};

// Attack properties
const attack = {
    width: 10,
    height: 10,
    speed: 10,
    active: false,
};

// Goal
const goal = {
    x: 0,
    y: 0,
    width: 32,
    height: 32,
};

// Enemies
const enemies = [];

// Walls
const walls = generateWalls();

// Score
let score = 0;

// // Function to handle updating top scores on the client
// function updateTopScores(newTopScores) {
//     alert(newTopScores);
//     const scoreList = document.getElementById('scoreList');
//     scoreList.innerHTML = '';
//     newTopScores.forEach((topScore, index) => {
//         const listItem = document.createElement('li');
//         listItem.textContent = `#${index + 1}: ${topScore}`;
//         scoreList.appendChild(listItem);
//     });
// }

// When a player dies, emit an event to request updated top scores
// Inside the game logic where a player's score is updated
function playerDied() {
    socket.emit('update_score', score, getCookie('Userid'), 'survive');
    score = 0; // Reset the score
    player.hp = 100; // Reset the player's HP
}


// Listen for the "top_scores_updated" event from the server
socket.on('score_updated', (newTopScores) => {
    let newline = "<br>"
    let scorelist = "";
    let topscores = document.getElementById("scoreList");
    for (var i = 0; i < newTopScores.length; i++) {
        var split = newTopScores[i].split(",");
        scorelist = scorelist + split + newline
    }
    topscores["innerHTML"] = scorelist;
});

// Get the skip button element by its ID
const skipButton = document.getElementById('skipButton');

// Add a click event listener to the button
skipButton.addEventListener('click', () => {
    // Call the generateNewLevel() function to skip to the next level
    generateNewLevel();
});

// Function to check if the player has touched the goal
function checkGoalCollision() {
    if (checkCollision(player, goal)) {
        // Player reached the goal
        score++;
        generateNewLevel();
    }
}


// Function to draw the score on the screen
function drawScore() {
    ctx.fillStyle = "#FFF";
    ctx.font = "24px Arial";
    ctx.fillText(`Score: ${score}`, 20, 70); // Adjust the position as needed
}

// Function to draw the score on the screen
function drawScore() {
    ctx.fillStyle = "#FFF";
    ctx.font = "24px Arial";
    ctx.fillText(`Score: ${score}`, 20, 70); // Adjust the position as needed

    // Update the scoreboard div with the current score
    const scoreboardDiv = document.getElementById('scoreboard');
    // scoreboardDiv.textContent = `Score: ${score}`;
}

// Game loop
function gameLoop() {
    movePlayer();
    moveEnemies();
    checkCollisions();
    checkGoalCollision(); // Check for goal collision
    drawGame();
    drawScore(); // Draw the score
    requestAnimationFrame(gameLoop);
}

// Function to generate a new level
function generateNewLevel() {
    // Clear existing walls and enemies
    walls.length = 0;
    enemies.length = 0;
    
    // Generate new walls for the next level
    walls.push(...generateWalls());

    // Randomly position the player avoiding walls
    positionPlayer();

    // Move the goal to a new random location, avoiding walls
    positionGoal();

    // Generate new enemies for the next level
    for (let i = 0; i < 5; i++) {
        enemies.push({
            x: Math.random() * SCREEN_WIDTH,
            y: Math.random() * SCREEN_HEIGHT,
            width: 32,
            height: 32,
            speed: 2,
        });
    }
}

// Generate random walls
function generateWalls() {
    const numWalls = 10;
    const generatedWalls = [];

    for (let i = 0; i < numWalls; i++) {
        const x = Math.random() * SCREEN_WIDTH;
        const y = Math.random() * SCREEN_HEIGHT;
        const width = Math.random() * 200 + 20;
        const height = Math.random() * 200 + 20;
        generatedWalls.push({ x, y, width, height });
    }

    return generatedWalls;
}

// Check if a point is inside a wall
function isPointInsideWall(x, y) {
    for (const wall of walls) {
        if (
            x >= wall.x &&
            x <= wall.x + wall.width &&
            y >= wall.y &&
            y <= wall.y + wall.height
        ) {
            return true;
        }
    }
    return false;
}

// Randomly position the player avoiding walls
function positionPlayer() {
    do {
        player.x = Math.random() * (SCREEN_WIDTH - player.width);
        player.y = Math.random() * (SCREEN_HEIGHT - player.height);
    } while (isPointInsideWall(player.x, player.y));
}

function checkCollision(rect1, rect2) {
    return (
        rect1.x < rect2.x + rect2.width &&
        rect1.x + rect1.width > rect2.x &&
        rect1.y < rect2.y + rect2.height &&
        rect1.y + rect1.height > rect2.y
    );
}

// Randomly position the goal avoiding walls
function positionGoal() {
    do {
        goal.x = Math.random() * (SCREEN_WIDTH - goal.width);
        goal.y = Math.random() * (SCREEN_HEIGHT - goal.height);
    } while (isPointInsideWall(goal.x, goal.y));
}

// Initialize player and goal positions
positionPlayer();
positionGoal();

// Move the player with WASD
function movePlayer() {
    const keys = keyState;
    const newX = player.x;
    const newY = player.y;

    if (keys["a"]) {
        newX -= player.speed;
    }
    if (keys["d"]) {
        newX += player.speed;
    }
    if (keys["w"]) {
        newY -= player.speed;
    }
    if (keys["s"]) {
        newY += player.speed;
    }

    // Check for collisions with walls
    if (!isCollidingWithWalls(newX, newY)) {
        player.x = newX;
        player.y = newY;
    }
}


// Move enemies toward the player
function moveEnemies() {
    for (const enemy of enemies) {
        const dx = player.x - enemy.x;
        const dy = player.y - enemy.y;
        const length = Math.max(Math.abs(dx), Math.abs(dy), 1);
        const normalizedDx = dx / length;
        const normalizedDy = dy / length;

        const new_x = enemy.x + normalizedDx * enemy.speed;
        const new_y = enemy.y + normalizedDy * enemy.speed;

        // Check for collisions with walls
        if (!isCollidingWithWalls(new_x, new_y)) {
            enemy.x = new_x;
            enemy.y = new_y;
        }
    }
}

// Check collisions
function checkCollisions() {
    // Check collisions with enemies
    for (const enemy of enemies) {
        if (
            player.x < enemy.x + enemy.width &&
            player.x + player.width > enemy.x &&
            player.y < enemy.y + enemy.height &&
            player.y + player.height > enemy.y
        ) {
            // Player and enemy collided, subtract HP
            const currentTime = Date.now();
            if (currentTime - player.lastHitTime > 10000) { // Check if 10 seconds have passed
                player.hp -= 10;
                player.lastHitTime = currentTime;
                player.knockback = 20; // Apply knockback
                if (player.hp <= 0) {
                    // Game over logic
                    generateNewLevel();
                    playerDied()
                    alert("Game over!");
                    // document.location.reload();
                }
            }
        }
    }
}

// Check collision with walls
function isCollidingWithWalls(newX, newY) {
    for (const wall of walls) {
        if (
            newX < wall.x + wall.width &&
            newX + player.width > wall.x &&
            newY < wall.y + wall.height &&
            newY + player.height > wall.y
        ) {
            return true;
        }
    }
    return false;
}
 
// Draw the game
function drawGame() {
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw walls
    ctx.fillStyle = WALL_COLOR;
    for (const wall of walls) {
        ctx.fillRect(wall.x, wall.y, wall.width, wall.height);
    }

    // Draw player
    ctx.fillStyle = PLAYER_COLOR;
    ctx.fillRect(player.x, player.y, player.width, player.height);

    // Draw enemies
    ctx.fillStyle = ENEMY_COLOR;
    for (const enemy of enemies) {
        ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
    }

    // Draw goal
    ctx.fillStyle = GOAL_COLOR;
    ctx.fillRect(goal.x, goal.y, goal.width, goal.height);

    // Display player HP
    ctx.fillStyle = "#FFF";
    ctx.font = "24px Arial";
    ctx.fillText(`HP: ${player.hp}`, 20, 40);

    // Draw attack if active
    if (attack.active) {
        ctx.fillStyle = "#F0F"; // Purple color for attack
        ctx.fillRect(attack.x, attack.y, attack.width, attack.height);
    }
}

// Key state tracking
const keyState = {};
window.addEventListener('keydown', (e) => {
    keyState[e.key] = true;
});
window.addEventListener('keyup', (e) => {
    keyState[e.key] = false;
});

// Generate initial enemies
for (let i = 0; i < 5; i++) {
    enemies.push({
        x: Math.random() * SCREEN_WIDTH,
        y: Math.random() * SCREEN_HEIGHT,
        width: 32,
        height: 32,
        speed: 2,
    });
}
 
// Start the game loop
gameLoop();
socket.emit("username", getCookie("Username"), 'games');
socket.emit('connect_game', 'survive');


});
