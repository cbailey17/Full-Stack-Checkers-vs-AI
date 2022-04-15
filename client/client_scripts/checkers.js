/* Author: Cameron Bailey */

const $ = require('jquery');


arr = Array.of(Array.of(Array.from(Array(24), (elem, idx) => (idx % 2 == 0) ? '.' : 'r')));
redcontainer = [arr[0].slice(0,8), arr[0].slice(9,16), arr[0].slice(17,24)];

arr = Array.of(Array.of(Array.from(Array(24), (elem, idx) => (idx % 2 == 0) ? '.' : 'b')));
blackcontainer = [arr[0].slice(0,8), arr[0].slice(9,16), arr[0].slice(17,24)];


//   ];
var gameBoard = [
    [{0:'.'}, {0:2}, {0:0}, {1:2}, {0:'.'}, {2:2}, {0:'.'}, {3:2}],
    [{4:2}, {0:'.'}, {5:2}, {0:'.'}, {6:2}, {0:'.'}, {7:2}, {0:'.'}],
    [{0:'.'}, {8:2}, {0:'.'}, {9:2}, {0:'.'}, {10:2}, {0:'.'}, {11:2}],
    [{12:'.'}, {0:'.'}, {13:'.'}, {0:'.'}, {14:'.'}, {0:'.'}, {15:'.'}, {0:'.'}],
    [{0:'.'}, {16:'.'}, {0:'.'}, {17:'.'}, {0:'.'}, {18:'.'}, {0:'.'}, {19:'.'}],
    [{20:1}, {0:'.'}, {21:1}, {0:'.'}, {22:1}, {0:'.'}, {23:1}, {0:'.'}],
    [{0:'.'}, {24:1}, {0:'.'}, {25:1}, {0:'.'}, {26:1}, {0:'.'}, {27:1}],
    [{28:1}, {0:'.'}, {29:1}, {0:'.'}, {30:1}, {0:'.'}, {31:1}, {0:'.'}]
  ];


//arrays to store the instances
var pieces = [];
var tiles = [];

//distance formula
var dist = (x1, y1, x2, y2) => Math.sqrt(Math.pow((x1 - x2), 2) + Math.pow((y1 - y2), 2));

class Tile {
    constructor(element, position) {
        this.element = element;
        this.position = position;

        this.inRange = (piece) => {
            for (let k of pieces)
                if (k.position[0] == this.position[0] && k.position[1] == this.position[1])
                    return 'wrong'; // same spot

            if (!piece.king && piece.player == 2 && this.position[0] < piece.position[0])
                return 'wrong';
            if (!piece.king && piece.player == 1 && this.position[0] > piece.position[0])
                return 'wrong';
            if (dist(this.position[0], this.position[1], piece.position[0], piece.position[1]) == Math.sqrt(2))
                return 'regular'; // regular move
            else if (dist(this.position[0], this.position[1], piece.position[0], piece.position[1]) == 2 * Math.sqrt(2))
                return 'jump'; // jump move
        };
    }
}

class Piece {
    constructor(element, position) {
        this.allowedToMove = true;
        this.element = element;
        this.position = position;
        this.player = '';

        if (this.element.attr("id") < 12) {
            this.player = 2;
            this.element.css("backgroundImage", "url('../img/ai.png')");
        }
        else 
            this.player = 1;

        this.makeKing = () => {
            this.element.css("backgroundImage", "url('../img/king" + this.player + ".png')");
            this.king = true;
        };
        this.move = (tile) => {
            this.element.removeClass('selected');
            if (!checkerBoard.isValidPlaceToMove(tile.position[0], tile.position[1]))
                return false;
            //make sure piece doesn't go backwards if it's not a king
            if (this.player == 2 && this.king == false) {
                if (tile.position[0] < this.position[0])
                    return false;
            } else if (this.player == 1 && this.king == false) {
                if (tile.position[0] > this.position[0])
                    return false;
            }
            // Object.values(checkerBoard.gameBoard[this.position[0]][this.position[1]])[0] = '.';
            Object.values(checkerBoard.gameBoard[tile.position[0]][tile.position[1]])[0] = this.player;

            Object.keys(checkerBoard.gameBoard[this.position[0]][this.position[1]]).forEach((key, index) => {
                checkerBoard.gameBoard[this.position[0]][this.position[1]][key] = '.';
            });
            Object.keys(checkerBoard.gameBoard[tile.position[0]][tile.position[1]]).forEach((key, index) => {
                checkerBoard.gameBoard[tile.position[0]][tile.position[1]][key] = this.player;
            });
         


            this.position = [tile.position[0], tile.position[1]];
            //change the css using board's dictionary
            this.element.css('top', checkerBoard.dictionary[this.position[0]]);
            this.element.css('left', checkerBoard.dictionary[this.position[1]]);
            //if piece reaches the end of the row on opposite side crown it a king (can move all directions)
            if (!this.king && (this.position[0] == 0 || this.position[0] == 7))
                this.makeKing();

            return true;
        }; 
        this.remove = () => {
            this.element.css("display", "none");
            if (this.player == 1)
                checkerBoard.score.player2 += 1;
            if (this.player == 2)
                checkerBoard.score.player1 += 1;
            // checkerBoard.gameBoard[this.position[0]][this.position[1]] = 0;
            Object.values(checkerBoard.gameBoard[this.position[0]][this.position[1]])[0] = '.';
            this.position = [];
            var playerWon = checkerBoard.checkIfAnybodyWon();
            if (playerWon)
                console.log("Player " + playerWon + " has won!");
        };
        this.canOpponentJump = (newPosition) => {
            var dx = newPosition[1] - this.position[1];
            var dy = newPosition[0] - this.position[0];
            //make sure object doesn't go backwards if not a king
            if (this.player == 1 && this.king == false) {
                if (newPosition[0] < this.position[0])
                    return false;
            } else if (this.player == 2 && this.king == false) {
                if (newPosition[0] > this.position[0])
                    return false;
            }
            //must be in bounds
            if (newPosition[0] > 7 || newPosition[1] > 7 || newPosition[0] < 0 || newPosition[1] < 0)
                return false;

            var tileToCheckx = this.position[1] + dx / 2;
            var tileToChecky = this.position[0] + dy / 2;

            if (tileToCheckx > 7 || tileToChecky > 7 || tileToCheckx < 0 || tileToChecky < 0)
                return false;
            //if there is a piece there and there is no piece in the space after that
            if (!checkerBoard.isValidPlaceToMove(tileToChecky, tileToCheckx) && checkerBoard.isValidPlaceToMove(newPosition[0], newPosition[1])) {
                //find which object instance is sitting there
                for (let pieceIndex in pieces) {
                    if (pieces[pieceIndex].position[0] == tileToChecky && pieces[pieceIndex].position[1] == tileToCheckx) {
                        if (this.player != pieces[pieceIndex].player)
                            //return the piece sitting there
                            return pieces[pieceIndex];
                    }
                }
            }
            return false;
        };
        //tests if piece can jump anywhere
        this.canJumpAny = () => {
            return (this.canOpponentJump([this.position[0] + 2, this.position[1] + 2]) ||
                this.canOpponentJump([this.position[0] + 2, this.position[1] - 2]) ||
                this.canOpponentJump([this.position[0] - 2, this.position[1] + 2]) ||
                this.canOpponentJump([this.position[0] - 2, this.position[1] - 2]));
        };
        this.opponentJump = (tile) => {
            var pieceToRemove = this.canOpponentJump(tile.position);
            //if there is a piece to be removed, remove it
            if (pieceToRemove) {
                pieceToRemove.remove();
                return true;
            }
            return false;
        };
    }
}



class Board {
    constructor(gameBoard, playerTurn, AI=true) {
        this.gameBoard = gameBoard;
        this.score = { player1: 0, player2: 0 };
        this.playerTurn = playerTurn;
        this.tileElements = $('div.tiles');
        this.dictionary = ["0vmin", "10vmin", "20vmin", "30vmin", "40vmin", "50vmin", "60vmin", "70vmin", "80vmin", "90vmin"]; 

        if (AI) 
            this.ai = new AIObject();

        this.initialize = () => {
            console.log("Initializing CheckerBoard....");
            var countPieces = 0;
            var countTiles = 0;
            
            for (let row in this.gameBoard) { 
                for (let column in this.gameBoard[row]) {
                    if (row % 2 == 1) { // row is odd 
                        if (column % 2 == 0) // column even
                            countTiles = this.tileRender(row, column, countTiles)
                    } else {
                        if (column % 2 == 1)
                            countTiles = this.tileRender(row, column, countTiles)
                    }
                if (Object.values(this.gameBoard[row][column])[0] == 1) 
                    countPieces = this.renderPieces(1, row, column, countPieces)
                else if (Object.values(this.gameBoard[row][column])[0] == 2) 
                    countPieces = this.renderPieces(2, row, column, countPieces)
                }
            }
        }
        this.tileRender = (row, column, countTiles) => {
            this.tileElements.append("<div class='tile' id='tile" + countTiles + "' style='top:" + this.dictionary[row] + ";left:" + this.dictionary[column] + ";'></div>");
            tiles[countTiles] = new Tile($("#tile" + countTiles), [parseInt(row), parseInt(column)]);
            return countTiles + 1
        }
        this.renderPieces = (playerNumber, row, column, countPieces) => {
            $(`.player${playerNumber}pieces`).append("<div class='piece' id='" + countPieces + "' style='top:" + this.dictionary[row] + ";left:" + this.dictionary[column] + ";'></div>");
            pieces[countPieces] = new Piece($("#" + countPieces), [parseInt(row), parseInt(column)]);
            return countPieces + 1;
        }
        this.returnPieces = () => {
            return {"tiles": tiles, "pieces": pieces};
        }
        this.isValidPlaceToMove = (row, column) => {
            if (row < 0 || row > 7 || column < 0 || column > 7) return false;
            if (Object.values(this.gameBoard[row][column])[0] == '.') {
                return true;
            }
            return false;
        }
        this.changePlayerTurn = () => {
            if (this.playerTurn == 1) 
                this.playerTurn = 2;
            else 
                this.playerTurn = 1;

            return this.playerTurn;
        }
        this.checkIfAnybodyWon = () => {
            if (this.score.player1 == 12) 
                return 1;
            else if (this.score.player2 == 12) 
            return 2;
            
            return false;
        }
        //reset the game
        this.clear = () => {
            location.reload();
        }
        this.checkIfJumpExists = () => {
            this.jumpExists = false;
        }
        this.visualizeString = (str) => {
            var vis = "  0 1 2 3 4 5 6 7 \n" 
                  + "0 " + str[0] + ' '+ str[1] + ' ' + str[2] +  ' ' + str[3] + ' ' + str[4] +  ' ' +  str[5] +  ' ' + str[6] +  ' ' +  str[7] +  ' ' +  '\n'
                  + "1 " + str[8] +  ' ' +  str[9] +  ' ' + str[10] +  ' ' +  str[11] +  ' ' +  str[12] +  ' ' +  str[13] +  ' ' +  str[14] +  ' ' +  str[15] + '\n'
                  + "2 " + str[16] +  ' ' +  str[17] +  ' ' + str[18] +  ' ' +  str[19] +  ' ' +  str[20] +  ' ' +  str[21] +  ' ' +  str[22] +  ' ' +  str[23] + '\n'
                  + "3 " + str[24] +  ' ' +  str[25] +  ' ' + str[26] +  ' ' +  str[27] +  ' ' +  str[28] +  ' ' +  str[29] +  ' ' +  str[30] +  ' ' +  str[31] + '\n'
                  + "4 " + str[32] +  ' ' +  str[33] +  ' ' + str[34] +  ' ' +  str[35] +  ' ' +  str[36] +  ' ' +  str[37] +  ' ' +  str[38] +  ' ' +  str[39] + '\n'
                  + "5 " + str[40] +  ' ' +  str[41] +  ' ' + str[42] +  ' ' +  str[43] +  ' ' +  str[44] +  ' ' +  str[45] +  ' ' +  str[46] +  ' ' +  str[47] + '\n'
                  + "6 " + str[48] +  ' ' +  str[49] +  ' ' + str[50] +  ' ' +  str[51] +  ' ' +  str[52] +  ' ' +  str[53] +  ' ' +  str[54] +  ' ' +  str[55] + '\n'
                  + "7 " + str[56] +  ' ' +  str[57] +  ' ' + str[58] +  ' ' +  str[59] +  ' ' +  str[60] +  ' ' +  str[61] +  ' ' +  str[62] +  ' ' +  str[63] + '\n';
            return vis;
        }

        this.boardToString = () => {
            var ret = ""
            for (let i in this.gameBoard) {
                for (let j in this.gameBoard[i]) {
                    var found = false
                    for (let k of pieces) {
                        if (k.position[0] == i && k.position[1] == j) {
                            if (k.king) ret += (Object.values(this.gameBoard[i][j]) + 2)
                            else ret += Object.values(this.gameBoard[i][j])
                            found = true
                            break
                        }
                    }
                    if (!found) ret += '.'
                }
            }
            return ret
        }
    }     
}

class AIObject {
    constructor() {
        this.playerNumber = 2;

        this.clearGameCache = async () => {
            const clearRes = await axios.post('http://localhost:3000/clearGameCache', {});
            console.log(clearRes.data);
            return clearRes;
        }
        this.initBackEndState = async () => {
            const initRes = await axios.post('http://localhost:3000/initializeBoard', {});
            console.log(initRes.data);
            return initRes;
        }
        this.getMove = async (action="none") => {
            const res = await axios.post('http://localhost:3000/', {
                action_str: action
              });
              console.log(res.data);
              console.log("New turn --------------------------------- ");
              return res;
        }
        this.getPiece = (move, checkerBoard) => {
            const checkerPosition = [move[6], move[9]]

            console.log(pieces);
            for (let piece of pieces) {
                if (piece.position.toString() == checkerPosition.toString())
                    return piece;
            }
            return {};
        }
        this.getTile = (move, checkerBoard) => {
            const tileRow = move[16];
            const tileColumn = move[19];
            const tileID = Object.keys(checkerBoard.gameBoard[tileRow][tileColumn])[0];
            const tileToMoveTo = $('#tile'+tileID);
            return tileToMoveTo;
        }
        this.makeMove = (move, checkerBoard) => {
            const checker_ = this.getPiece(move, checkerBoard);
            const tile_ = this.getTile(move, checkerBoard);
            const destinationTile = tiles[moveTile[0].id.replace(/tile/, '')];
            computersPiece.move(destinationTile);
        }
    }
}
var checkerBoard = new Board(gameBoard, 1, true);
checkerBoard.initialize();
module.exports = checkerBoard;

$('.start').on('click', async () => {
    checkerBoard.ai.initBackEndState();
});

window.addEventListener('load', async (event) => {
    await checkerBoard.ai.initBackEndState();
  });
  

$('.reset').on('click', async () => {

    await checkerBoard.ai.clearGameCache();
    checkerBoard.clear();
})

// Handle events
$('.piece').on("click", function () {
    if ($(this).parent()[0].classList.contains('player2pieces'))
        return;
    var selected;
    var isPlayersTurn = true;
    if (isPlayersTurn) {
      if (pieces[$(this).attr("id")].allowedToMove) {
        if ($(this).hasClass('selected')) selected = true;
        $('.piece').each(function (index) {
            $('.piece').eq(index).removeClass('selected')
        });
        if (!selected)
          $(this).addClass('selected');
      } 
    }
  });

$('.tile').on("click", async (elem) => {
    if ($('.selected').length != 0) {
        let str = checkerBoard.boardToString();
        console.log(checkerBoard.visualizeString(str));

        var tileId = elem.currentTarget.id.replace(/tile/, '');
        var tile = tiles[tileId];
        var pieceSelected = pieces[$('.selected').attr("id")];
        var originalPosition = pieceSelected.position;
        var successfulMove = false;


        var possibleMove = tile.inRange(pieceSelected);
        if (possibleMove != 'wrong') {
            if (possibleMove == 'jump') {
                if (pieceSelected.opponentJump(tile)) {
                    pieceSelected.move(tile);
                    successfulMove = true;

                    if (pieceSelected.canJumpAny()) {
                        pieceSelected.element.addClass('selected');
                        checkerBoard.continuousJump = true;
                    } else 
                        checkerBoard.changePlayerTurn();
                }
            } else if (possibleMove == 'regular' && !checkerBoard.jumpExists) {
                if (!pieceSelected.canJumpAny()) {
                    pieceSelected.move(tile);
                    successfulMove = true;

                    Object.keys(gameBoard[tile.position[0]][tile.position[1]]).forEach((key, index) => {
                        gameBoard[tile.position[0]][tile.position[1]][key] = 1;
                    });
                    Object.keys(gameBoard[originalPosition[0]][originalPosition[1]]).forEach((key, index) => {
                        gameBoard[originalPosition[0]][originalPosition[1]][key] = '.';
                    });
                    checkerBoard.changePlayerTurn();
                } else 
                    console.log("You must jump when possible");
            }
        }
    }

    if (successfulMove) {
        let action_str = `from (${originalPosition[0]+', '+originalPosition[1]}) to (${pieceSelected.position[0]+', '+pieceSelected.position[1]})`;
        console.log(action_str);
    
        const nextMove = await checkerBoard.ai.getMove(action_str);
        const computersPiece = checkerBoard.ai.getPiece(nextMove.data, checkerBoard);
        const moveTile = checkerBoard.ai.getTile(nextMove.data, checkerBoard);
        const destinationTile = tiles[moveTile[0].id.replace(/tile/, '')];
        console.log(destinationTile);
    
        Object.keys(gameBoard[computersPiece.position[0]][computersPiece.position[1]]).forEach((key, index) => {
            gameBoard[computersPiece.position[0]][computersPiece.position[1]][key] = '.';
        });
        computersPiece.move(destinationTile);
        Object.keys(gameBoard[computersPiece.position[0]][computersPiece.position[1]]).forEach((key, index) => {
            console.log(checkerBoard.playerTurn)
            if (checkerBoard.playerTurn == 1)
                gameBoard[computersPiece.position[0]][computersPiece.position[1]][key] = 1;
            else
                gameBoard[computersPiece.position[0]][computersPiece.position[1]][key] = 2; 
        });
        checkerBoard.changePlayerTurn();
        console.log(checkerBoard);
        console.log(checkerBoard.visualizeString(checkerBoard.boardToString()))
    }
});



