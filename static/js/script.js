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
const currentPlayer =  document.body.getAttribute('data-player-type');//document.querySelector('p.message').textContent.split(' ')[2];
const socket = new WebSocket('ws://' + window.location.host + '/ws/match/');
// const currentPlayer = document.querySelector('.current-player').textContent;
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
    if (this.playerTurn !== 'Creator') {  // Modify as per your needs
        this.displayMessage("It's not your turn!");
        this.toggleCheckButton(false);  // Disable the button
        return;
    }

    // Check if the player hasn't inputted a number
    else if (!guess) {
        this.displayMessage("You didn't input Number");
        return;
    }

    // Check if the player's guess is correct
    else if (guess === this.number) {
        socket.send(JSON.stringify({
                'action': 'player_win',
                'game_id': game_id  // Assuming you've saved the game_id on the client side.
            }));
        this.correctGuess();
    }
    // If the player's guess is wrong
    else if (guess !== this.number) {
        this.swapTurn();
        socket.send(JSON.stringify({
                'action': 'turn_end',
                'game_id': game_id  // Assuming you've saved the game_id on the client side.
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


    correctGuess() {
        // this.displayMessage("Correct Answer");
        // document.querySelector('body').style.backgroundColor = '#60b347';
        // document.querySelector('.number').textContent = this.number;
        // document.querySelector('.number').style.width = '30rem';
        this.displayMessage("Correct Answer");
        document.querySelector('body').style.opacity = '0';

        setTimeout(() => {
            // Slowly reveal the correct number and enlarge it
            document.querySelector('body').style.backgroundColor = '#60b347';
            document.querySelector('body').style.opacity = '1';
            document.querySelector('.number').textContent = this.number;

            // document.querySelector('.number').style.fontSize = '30rem';
            document.querySelector('.number').style.width = '30rem'; // Adjust width
            // document.querySelector('.number').style.height = '30rem'; // Adjust height considering padding

            document.querySelector('body').classList.add('fireworks');
        }, 1000);
        // Set new highscore if necessary
        if (this.score > this.highscore) {
            this.highscore = this.score;
            document.querySelector('.highscore').textContent = this.highscore;
        }
    }

    wrongGuess(guess) {
        if (this.score > 1) {
            this.displayMessage(guess > this.number ? "Too high" : "Too low");
            this.score--;
            document.querySelector('.score').textContent = this.score;
        } else {
            this.displayMessage("You lost the game");
            document.querySelector('.score').textContent = 0;
        }
    }

    displayMessage(message) {
        document.querySelector('.message').textContent = message;
        document.querySelector('.message').textContent = `Player ${this.playerTurn}: ${message}`;
    }

    resetGame() {
        document.querySelector('body').classList.remove('fireworks'); // Remove fireworks effect
        this.number = this.generateRandomNumber();
        this.playerTurn = this.playerTurn === 'player1' ? 'player2' : 'player1';
        this.score = 20;
        document.querySelector('.score').textContent = this.score;
        document.querySelector('.guess').value = '';
        document.querySelector('.number').textContent = '?';
        document.querySelector('.message').textContent = 'Start guessing...';
        document.querySelector('body').style.backgroundColor = '#222';
        document.querySelector('.number').style.fontSize = '15rem';
    }
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

    if (data.action === 'turn_notification' && data.next_turn === 'player1') {
        game.playerTurn = 'player1';
        game.toggleCheckButton(true);
        game.displayMessage('Your turn!');
    } else if (data.action === 'turn_notification' && data.next_turn === 'player2') {
        game.playerTurn = 'player2';
        game.toggleCheckButton(true);
        game.displayMessage('Your turn!');
    } else if (data.action === 'not_your_turn') {
        game.toggleCheckButton(false);
        game.displayMessage('Waiting for the other player...');
    }
    // ... other possible actions ...
};

// socket.onclose = function(e) {
//     console.error('WebSocket closed unexpectedly');
// };
const game = new Game();

document.querySelector('.check').addEventListener('click', function() {
    game.checkGuess();
});

document.querySelector('.again').addEventListener('click', function() {
    game.resetGame();
});