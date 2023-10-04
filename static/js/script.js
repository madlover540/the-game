// 'use strict';

// // console.log(document.querySelector('.message').textContent);

// // document.querySelector('.message').textContent = "Correct Number";
// // document.querySelector('.number').textContent = 13;
// // document.querySelector('.score').textContent = 10;
// // document.querySelector('.guess').value
// const number = Math.trunc(Math.random() * 20) + 1;
// console.log(number)
// document.querySelector('.check').addEventListener('click', function() {
//     const guess = Number(document.querySelector('.guess').value);
//     let userscore = Number(document.querySelector('.score').textContent);
//     console.log('userscore', userscore)

//     document.querySelector('.score').textContent = userscore
//         // console.log(typeof guess)
//     if (!guess) {
//         document.querySelector('.message').textContent = "You didn't input Number";
//     } else if (guess === number) {
//         document.querySelector('.message').textContent = "Correct Answer";
//         document.querySelector('body').style.backgroundColor = '#60b347';
//         document.querySelector('.number').textContent = number;
//         document.querySelector('.number').style.width = '30rem';
//     } else if (guess > number) {
//         document.querySelector('.message').textContent = "Too high";
//         if (userscore > 1) {
//             userscore -= 1;
//             document.querySelector('.score').textContent = userscore

//         } else if (userscore === 1) { document.querySelector('.message').textContent = "You lost the game" }
//     } else if (guess < number) {
//         document.querySelector('.message').textContent = "Too low";
//         if (userscore > 1) {
//             userscore -= 1;
//             document.querySelector('.score').textContent = userscore
//         } else if (userscore === 0) { document.querySelector('.message').textContent = "You lost the game" };
//     } else {
//         document.querySelector('.message').textContent = "Wrong Answer";

//     }
// });
const game_id = document.querySelector('h1.game_id').textContent.split(' ')[2];
const currentPlayer = document.body.getAttribute('data-player-type');

// Use wss:// if HTTPS, otherwise use ws://
const socket = new WebSocket(
    location.protocol === 'https:' ? `wss://${window.location.host}/ws/match/` : `ws://${window.location.host}/ws/match/`
);

class Game {
    constructor() {
        this.playerTurn = currentPlayer;
        this.number = this.generateRandomNumber();
        this.score = 20;
        this.highscore = 0;
    }

    generateRandomNumber() {
        return Math.trunc(Math.random() * 20) + 1;
    }

    checkGuess() {
        const guess = Number(document.querySelector('.guess').value);

        // Check if it's the player's turn
        if (this.playerTurn !== currentPlayer) {
            this.displayMessage("It's not your turn!");
            this.toggleCheckButton(false);  // Disable the button
            return;
        }

        // Check if the player hasn't inputted a number
        if (!guess) {
            this.displayMessage("You didn't input Number");
            return;
        }

        // Check if the player's guess is correct
        if (guess === this.number) {
            socket.send(JSON.stringify({
                'action': 'player_win',
                'game_id': game_id
            }));
            this.correctGuess();
        } else {  // If the player's guess is wrong
            this.swapTurn();
            socket.send(JSON.stringify({
                'action': 'turn_end',
                'game_id': game_id
            }));
            this.wrongGuess(guess);
        }
    }

    toggleCheckButton(enable) {
        const btnCheck = document.querySelector('.btn.check');
        if (enable) {
            btnCheck.removeAttribute('disabled');
        } else {
            btnCheck.setAttribute('disabled', 'disabled');
        }
    }

    // ... [rest of the Game class methods remain unchanged] ...

    swapTurn() {
        this.playerTurn = this.playerTurn === 'player1' ? 'player2' : 'player1';
        if (this.playerTurn === currentPlayer) {
            this.toggleCheckButton(true);
            this.displayMessage('Your turn!');
        } else {
            this.toggleCheckButton(false);
            this.displayMessage('Waiting for the other player...');
        }
    }
}

socket.onopen = function(e) {
    socket.send(JSON.stringify({
        'action': 'start_game',
        'game_id': game_id
    }));
};

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    if (data.action === 'turn_notification') {
        if (data.next_turn === currentPlayer) {
            game.playerTurn = currentPlayer;
            game.toggleCheckButton(true);
            game.displayMessage('Your turn!');
        } else {
            game.toggleCheckButton(false);
            game.displayMessage('Waiting for the other player...');
        }
    }
    // ... other possible actions ...
};

socket.onclose = function(e) {
    console.error('WebSocket closed unexpectedly');
    // Maybe display a message to the user about the disconnection.
};

const game = new Game();

document.querySelector('.check').addEventListener('click', function() {
    game.checkGuess();
});

document.querySelector('.again').addEventListener('click', function() {
    game.resetGame();
});
