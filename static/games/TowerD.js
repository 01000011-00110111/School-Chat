document.addEventListener('DOMContentLoaded', function () {
    // Constants
    const SCREEN_WIDTH = 800;
    const SCREEN_HEIGHT = 600;
    const TOWER_COLOR = "#00F";
    const ENEMY_COLOR = "#F00";
    const GOAL_COLOR = "#0F0"; // Color for the goal

    // Initialize canvas
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    // Towers
    const towers = [];

    // Enemies
    const enemies = [];

    // Score
    let score = 0;

    // Function to draw the score on the screen
    function drawScore() {
        ctx.fillStyle = "#FFF";
        ctx.font = "24px Arial";
        ctx.fillText(`Score: ${score}`, 20, 70); // Adjust the position as needed
    }

    // Game loop
    function gameLoop() {
        moveEnemies();
        attackEnemies();
        moveTowers();
        checkCollisions();
        drawGame();
        drawScore();
        updateUI();
        requestAnimationFrame(gameLoop);
    }

    // Function to move towers
    function moveTowers() {
        for (const tower of towers) {
            for (const enemy of enemies) {
                const distance = Math.sqrt(Math.pow((tower.x - enemy.x), 2) + Math.pow((tower.y - enemy.y), 2));
                if (distance <= tower.range) {
                    enemy.health -= tower.damage;
                    if (enemy.health <= 0) {
                        score += 10;
                        const index = enemies.indexOf(enemy);
                        if (index !== -1) {
                            enemies.splice(index, 1);
                        }
                    }
                }
            }
        }
    }

    // Function to move enemies
    function moveEnemies() {
        for (const enemy of enemies) {
            if (enemy.pathIndex < enemyPath.length) {
                const targetX = enemyPath[enemy.pathIndex].x;
                const targetY = enemyPath[enemy.pathIndex].y;
                const dx = targetX - enemy.x;
                const dy = targetY - enemy.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                const speed = 2;
                if (distance > speed) {
                    enemy.x += (dx / distance) * speed;
                    enemy.y += (dy / distance) * speed;
                } else {
                    enemy.pathIndex++;
                }
            } else {
                deductHP();
                const index = enemies.indexOf(enemy);
                if (index !== -1) {
                    enemies.splice(index, 1);
                }
            }
        }
    }

    // Function to check collisions
    function checkCollisions() {
        for (const projectile of projectiles) {
            for (const enemy of enemies) {
                const distance = Math.sqrt(Math.pow((projectile.x - enemy.x), 2) + Math.pow((projectile.y - enemy.y), 2));
                if (distance <= projectile.range) {
                    enemy.health -= projectile.damage;
                    if (enemy.health <= 0) {
                        score += 10;
                        const index = enemies.indexOf(enemy);
                        if (index !== -1) {
                            enemies.splice(index, 1);
                        }
                    }
                    const pIndex = projectiles.indexOf(projectile);
                    if (pIndex !== -1) {
                        projectiles.splice(pIndex, 1);
                    }
                }
            }
        }
    }

    // Function to draw the game
    function drawGame() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = TOWER_COLOR;
        for (const tower of towers) {
            ctx.fillRect(tower.x, tower.y, tower.width, tower.height);
        }
        ctx.fillStyle = ENEMY_COLOR;
        for (const enemy of enemies) {
            ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
        }
        ctx.fillStyle = GOAL_COLOR;
        ctx.fillRect(goal.x, goal.y, goal.width, goal.height);
    }

    // Start the game loop
    gameLoop();

    // Fetch top scores from the server and update the leaderboard
    function updateLeaderboard() {
        // Use fetch or AJAX to get the top scores from the server
        // Parse the response and update the leaderboard HTML element
        const leaderboard = document.getElementById('scoreList');
        leaderboard.innerHTML = '';
        // Loop through the top scores and add them to the leaderboard
        // Example: leaderboard.innerHTML += `<li>${scoreData.username}: ${scoreData.score}</li>`;
    }

    // Call the updateLeaderboard function to initially load the top scores
    updateLeaderboard();

    // You can periodically call updateLeaderboard to refresh the scores
    setInterval(updateLeaderboard, 5000); // Refresh every 5 seconds

    // Define Tower Types
    const towerTypes = [
        { name: "Tower A", cost: 50, damage: 10, range: 100 },
        { name: "Tower B", cost: 75, damage: 15, range: 120 },
        // Add more tower types here
    ];

    // UI Elements
    let money = 100;
    let selectedTower = null;

    // Function to update UI elements
    function updateUI() {
        document.getElementById('moneyValue').textContent = money;
        document.getElementById('scoreValue').textContent = score;
        document.getElementById('waveValue').textContent = wave;
        document.getElementById('hpValue').textContent = hp;
    }

    // Function to buy towers
    function buyTower(towerIndex) {
        const towerType = towerTypes[towerIndex];
        if (money >= towerType.cost) {
            selectedTower = towerType;
        }
    }

    // Listen for canvas clicks to place towers
    canvas.addEventListener('click', (event) => {
        if (selectedTower) {
            money -= selectedTower.cost;
            selectedTower = null;
        }
    });

    // Enemy Path
    const enemyPath = [
        { x: 100, y: 100 },
        { x: 200, y: 100 },
        { x: 200, y: 200 },
        // Add more path points
    ];

    // Function to spawn a wave of enemies
    function spawnWave() {
        // Spawn enemies for the current wave
        wave++;
    }

    // Function to deduct HP when enemies reach the end
    function deductHP() {
        hp -= 10;
        if (hp <= 0) {
            alert("Game over!");
        }
    }

    let hp = 100;
    let wave = 1;

    // Function to attack enemies
    function attackEnemies() {
        // Implement tower attack logic
    }

    // Fetch the initial top scores when the page loads
    socket.on('connect', () => {
        socket.emit('get_top_scores');
    });

    // Function to handle updating top scores on the client
    function updateTopScores(newTopScores) {
        const scoreList = document.getElementById('scoreList');
        scoreList.innerHTML = '';
        newTopScores.forEach((topScore, index) => {
            const listItem = document.createElement('li');
            listItem.textContent = `#${index + 1}: ${topScore}`;
            scoreList.appendChild(listItem);
        });
    }

    // Listen for the "top_scores_updated" event from the server
    socket.on('score_updated', (newTopScores) => {
        updateTopScores(newTopScores);
    });
});
