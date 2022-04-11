

var tiles = document.querySelectorAll('td');
var redPieces = document.querySelectorAll('p');
var blackPieces = document.querySelectorAll('span');

// player properties
let turn = true;
let redScore = 12;
let blackScore = 12;
let playerPieces;

const board = [
    null, 0, null, 1, null, 2, null, 3,
    4, null, 5, null, 6, null, 7, null,
    null, 8, null, 9, null, 10, null, 11,
    null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null,
    12, null, 13, null, 14, null, 15, null,
    null, 16, null, 17, null, 18, null, 19,
    20, null, 21, null, 22, null, 23, null
];

for (let i = 0; i <= 23; i++) {
    board.push(null);
    board.push(i);
} board.push(null);


function setCheckerEvents() {
    blackPieces.forEach(element => {
        element.addEventListener('click', activateChecker);
    });
    redPieces.forEach(element => {
        element.addEventListener('click', activateChecker);
    });
}

function removeCheckerEvents() {
    blackPieces.forEach(element => {
        element.removeAttribute('onclick');
    });
    redPieces.forEach(element => {
        element.removeAttribute('onclick');
    });
}

function activateChecker(checker) {
    checker.target.style.height = '27px';
    checker.target.style.width = '27px';
    checker.target.classList.add('active');
    waitForAndExecuteMove();
    removeCheckerEvents();
}

function waitForAndExecuteMove() {
    tiles.addEventListener('click', moveChecker);
}

function moveChecker() {
    let activatedChecker = document.querySelector('active');

}

async function getComputersMove() {
    try {
        await axios.get('http://localhost:3000')
            .then(response => console.log(response))
            .catch(error => console.log(error))
            .then(() => console.log("Hello"))
    } catch(error) {
        console.log(error);
    }
}

getComputersMove();
setCheckerEvents();
