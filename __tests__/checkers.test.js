const $ = require('jquery');
const Board = require('../client/client_scripts/checkers');


// console.log(Board.visualizeString(Board.boardToString()));
// console.log(Board);
// console.log(Board.returnPieces())

describe('test board class', () => {
    let pieces = Board.returnPieces().pieces;
    let tiles = Board.returnPieces().tiles;
    let moves = [
        [2,7,6,6]
    ] 
    for (tile of tiles) {
        if (tile.position[0] == moves[0][0] && tile.position[1] == moves[0][1]){
            expect(Object.values(Board.gameBoard[moves[0][0]][moves[0][1]])[0]).toBe(2)
        }
    }
    test('test tile location', () => {
        // for (let i = 0; )
        console.log(Board.returnPieces())
    });

    test('Changing players turns 100 times works test', () => {
        player = 1;
        for (let i = 0; i < 100; i++) {
            let turn = Board.changePlayerTurn(player);
            expect(turn).toBe(2);
            Board.changePlayerTurn(player);
        }
    });
});