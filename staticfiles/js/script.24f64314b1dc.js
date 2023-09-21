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

class Game {
    constructor() {
        this.number = this.generateRandomNumber();
        this.score = 20;
        this.highscore = 0;
    }

    generateRandomNumber() {
        return Math.trunc(Math.random() * 20) + 1;
    }

    checkGuess() {
        const guess = Number(document.querySelector('.guess').value);
        if (!guess) {
            this.displayMessage("You didn't input Number");
        } else if (guess === this.number) {
            this.correctGuess();
        } else if (guess !== this.number) {
            this.wrongGuess(guess);
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
    }

    resetGame() {
        document.querySelector('body').classList.remove('fireworks'); // Remove fireworks effect
        this.number = this.generateRandomNumber();
        this.score = 20;
        document.querySelector('.score').textContent = this.score;
        document.querySelector('.guess').value = '';
        document.querySelector('.number').textContent = '?';
        document.querySelector('.message').textContent = 'Start guessing...';
        document.querySelector('body').style.backgroundColor = '#222';
        document.querySelector('.number').style.fontSize = '15rem';
    }
}

const game = new Game();

document.querySelector('.check').addEventListener('click', function() {
    game.checkGuess();
});

document.querySelector('.again').addEventListener('click', function() {
    game.resetGame();
});