function setupIA() {

const canvas = document.querySelector("#pongIaCanvas");
const ctx = canvas.getContext('2d');

const paddleWidth = 10;
const paddleHeight = 100;
const paddleSpeed = 4;
const initialBallSpeed = 4;
const maxBallSpeed = 6;
const keyState = {};

var TimeStart = Date.now();

let player1Score = 0;
let computerScore = 0;


let player1Y = canvas.height / 2 - paddleHeight / 2;
let player1X = canvas.width;

const ball = {
    x: canvas.height / 2, 
    y: canvas.height/2,
    radius: 10, 
    speed: 4, 
    dx: 4, 
    dy: 4
}

const aiPaddle = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    width: 10,
    height: 100,
    dy: 4,
};

//Fonction pour dessiner des rectangles
function drawRect(x, y, width, height, color) {
    ctx.fillStyle = color;
    ctx.fillRect(x, y, width, height);
}

// Fonction pour dessiner une ligne au milieu
function drawLine() {
    ctx.strokeStyle = 'white';
    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.stroke();
}

//Fonction pour dessiner un cercle
function drawCircle(x, y, radius, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();
}

//Fonction pour écrire du texte
function drawText(text, x, y, color, font = '20px Arial') {
    ctx.fillStyle = color;
    ctx.font = font;
    ctx.fillText(text, x, y);
}

function draw() {
    // Nettoyer le canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Dessiner les deux joueurs
    drawRect(0, player1Y, paddleWidth, paddleHeight, 'white');
    drawRect(canvas.width - paddleWidth, aiPaddle.y, paddleWidth, paddleHeight, 'white');

    //Dessiner la ligne du milieu
    drawLine();

    // Dessiner la balle
    drawCircle(ball.x, ball.y, ball.radius, 'white');

    // Ecrire les scores
    document.getElementById("player1-score").textContent = player1Score;
    document.getElementById("player2-score").textContent = computerScore;

    moveBall();
}

function getRandomNumber(min, max) {
    return Math.random() * (max - min) + min;
}

// Fonction pour la direction vers le haut à gauche
function startTopLeft(ballX, ballY) {
    if (Math.random() < 0.5)
    {
        ball.dx = -1 * initialBallSpeed;
        ball.dy = -1 * initialBallSpeed;
    }
    else
    {
        ball.dx = -1 * initialBallSpeed;
        ball.dy = -1.4 * initialBallSpeed;
    }
}

// Fonction pour la direction vers le haut à droite
function startTopRight(ballX, ballY) {
    if (Math.random() < 0.5)
    {
        ball.dx = 1 * initialBallSpeed;
        ball.dy = -1 * initialBallSpeed;
    }
    else
    {
        ball.dx = 1 * initialBallSpeed;
        ball.dy = -0.5 * initialBallSpeed;
    }
}

// Fonction pour la direction vers le bas à gauche
function startBottomLeft(ballX, ballY) {
    if (Math.random() < 0.5)
    {
        ball.dx = -1 * initialBallSpeed;
        ball.dy = 1 * initialBallSpeed;
    }
    else
    {
        ball.dx = -1 * initialBallSpeed;
        ball.dy = 1.4 * initialBallSpeed;
    }
}

// Fonction pour la direction vers le bas à droite
function startBottomRight(ballX, ballY) {
    if (Math.random() < 0.5)
    {
        ball.dx = 1 * initialBallSpeed;
        ball.dy = 1 * initialBallSpeed; 
    }
    else
    {
        ball.dx = 1 * initialBallSpeed;
        ball.dy = 1.4 * initialBallSpeed;
    }
}

// Choisir une direction de manière aléatoire
function chooseRandomDirection(ballX, ballY) {
    const directions = [
        startTopLeft,
        startTopRight,
        startBottomLeft,
        startBottomRight
    ];
    const randomIndex = Math.floor(Math.random() * directions.length);
    const randomDirectionFunction = directions[randomIndex];
    randomDirectionFunction(ballX, ballY);
}

//Replacer la balle au centre
function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.dx = initialBallSpeed;
    ball.dy = initialBallSpeed;
    chooseRandomDirection(ball.x, ball.y);
}

function resetPaddles() {
    player1Y = (canvas.height - paddleHeight) / 2;
    aiPaddle.y = (canvas.height - paddleHeight) / 2;
}


// mise à jour de l'état des touches
function handleKeydown(event) {
    keyState[event.key] = true;
}

function handleKeyup(event) {
    keyState[event.key] = false;
}

//Déplacer les joueurs selon les touches du clavier
function handleKeyPress() {

    if (keyState["ArrowUp"] && player1Y > 0)
        player1Y -= paddleSpeed;
    if (keyState["ArrowDown"] && player1Y < canvas.height - paddleHeight)
        player1Y += paddleSpeed;
}


function moveBall() {
    ball.x += ball.dx;
    ball.y += ball.dy;


        if ((ball.y + ball.radius >= canvas.height || ball.y - ball.radius <= 0)) {
            ball.dy = -ball.dy * getRandomNumber(0.8, 1.2);
            ball.y += ball.dy;
        }
    
        // Envoyer la balle de l'autre côté si elle touche un joueur
        else if (ball.x - ball.radius < paddleWidth &&
            ball.y + ball.radius > player1Y &&
            ball.y - ball.radius < player1Y + paddleHeight) {
            ball.dx = -ball.dx * getRandomNumber(0.8, 1.2); //0,8, 1,2
            ball.x += ball.dx;
            adjustAiTarget();
        }
    
        else if (ball.x + ball.radius > canvas.width - paddleWidth &&
            ball.y + ball.radius > aiPaddle.y &&
            ball.y - ball.radius < aiPaddle.y + paddleHeight) {
            ball.dx = -ball.dx * getRandomNumber(0.8, 1.2);
            ball.x += ball.dx;
            adjustAiTarget();
    
        }

        if (ball.x + ball.radius > canvas.width)
        {
            player1Score++;
            resetBall();
            resetPaddles();
        }
        if (ball.x - ball.radius < 0)
        {
            computerScore++;
            resetBall();
            resetPaddles();
        }


        if (Math.abs(ball.dx) < maxBallSpeed) {
            ball.dx += ball.dx > 0 ? 0.001 : -0.001;
        }
        else
        {
            ball.dx = maxBallSpeed;
        }
    
        if (Math.abs(ball.dy) < maxBallSpeed) {
            ball.dy += ball.dy > 0 ? 0.001 : -0.001;
        }
        else
        {
            ball.dy = maxBallSpeed;
        }
}

function movePaddle(paddle, y) 
{
    paddle.y = y;
    if (paddle.y < 0) paddle.y = 0;
    if (paddle.y + paddleHeight > canvas.height) paddle.y = canvas.height - paddleHeight;
}

let aiTargetY = canvas.height / 2;
function adjustAiTarget() {
    if (aiPaddle.y + aiPaddle.height / 2 - ball.y < 10)
        aiTargetY = aiTargetY + 4;
    else if (aiPaddle.y + aiPaddle.height / 2 - ball.y > 10)
        aiTargetY = aiTargetY - 4;
}

/*function aiLogic_back() {
    if (ball.dx > 0){

    
        adjustAiTarget();

        movePaddle(aiPaddle, aiTargetY );
        /*
        if (aiPaddle.y + aiPaddle.height / 2 < aiTargetY)
        {
            movePaddle(aiPaddle, aiPaddle.y + aiPaddle.dy);
        }
        else 
            movePaddle(aiPaddle, aiPaddle.y - aiPaddle.dy);
        
    }
}*/

var lastUpadateAt = null;
var pY = 100;


function aiLogic() {
    if(lastUpadateAt === null || (Date.now() - lastUpadateAt > 1000))
    {
       lastUpadateAt = Date.now();
        pY = predictY(ball);   
     }
        
    if (aiPaddle.y + aiPaddle.height / 2 - pY < 10)
        movePaddle(aiPaddle, aiPaddle.y + aiPaddle.dy);
    else if (aiPaddle.y + aiPaddle.height / 2 + pY > 10)
        movePaddle(aiPaddle, aiPaddle.y - aiPaddle.dy);    
}


// Boucle sur le jeu 
function gameLoop() {
    if (location.pathname != '/ia/') {
        return ;
    }
    if (TimeStart == null) {
        TimeStart = Date.now();
    }
    aiLogic();
    draw();
    handleKeyPress();

    if (player1Score < 5 && computerScore < 5) {
        requestAnimationFrame(gameLoop);
    } else {
        endGame();
    }
}

//Predire la posotion de la balle
function predictY(ball) {
    let bx = ball.x 
    let by = ball.y

    let bdx = ball.dx 
    let bdy = ball.dy
    
    while(1)
    {
        bx += bdx;
        by +=bdy;

        if ((by + ball.radius >= canvas.height || by - ball.radius <= 0)) {
           bdy = -bdy * getRandomNumber(0.6, 1.4);
            by +=bdy;
        }
        // Envoyer la balle de l'autre côté si elle touche un joueur
        else if (bx - ball.radius < paddleWidth) {
            bdx = -bdx * getRandomNumber(0.6, 1.4); //0,8, 1,2
            bx += bdx;
        }
        else if (bx + ball.radius > canvas.width - paddleWidth ) {     
                return by;
        }
    }
}

function endGame() {
    var TimeEnd = Date.now() - TimeStart;
    if (player1Score === 5) {
        fetch(updateScoreUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'winner_uid': userId,
                'score': player2Score,
                'time': TimeEnd
            })
        }).then(response => {
            if (response.ok) {
                console.log('Score updated successfully!');
                setTimeout(() => {
                    loadView(gamepageUrl);
                }, 2000);
            } else {
                console.error('Failed to update score!');
            }
        }).catch(error => {
            console.error('Error updating score:', error);
        });

        drawText(username + " wins !", 350, 250, 'red');
    } else {
        fetch(updateLoseUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'winner_uid': '0',
                'score': player1Score,
                'time': TimeEnd
            })
        }).then(response => {
            if (response.ok) {
                console.log('Score updated successfully!');
                setTimeout(() => {
                    loadView(gamepageUrl);
                }, 2000);
            } else {
                console.error('Failed to update score!');
            }
        }).catch(error => {
            console.error('Error updating score:', error);
        });

        drawText("Player 2 wins !", 350, 250, 'red');
    }
}

document.addEventListener('keydown', handleKeydown);
document.addEventListener('keyup', handleKeyup);
gameLoop();
}