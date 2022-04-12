/* Author: Cameron Bailey */

var gameBoard = [
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 2, 0]
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

            if (!piece.king && piece.player == 1 && this.position[0] < piece.position[0])
                return 'wrong';
            if (!piece.king && piece.player == 2 && this.position[0] > piece.position[0])
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

        if (this.element.attr("id") < 12)
            this.player = 1;

        else
            this.player = 2;
        this.makeKing = () => {
            this.element.css("backgroundImage", "url('../img/king" + this.player + ".png')");
            this.king = true;
        };
        this.move = (tile) => {
            this.element.removeClass('selected');
            if (!checkerBoard.isValidPlaceToMove(tile.position[0], tile.position[1]))
                return false;
            //make sure piece doesn't go backwards if it's not a king
            if (this.player == 1 && this.king == false) {
                if (tile.position[0] < this.position[0])
                    return false;
            } else if (this.player == 2 && this.king == false) {
                if (tile.position[0] > this.position[0])
                    return false;
            }
            //remove the mark from Board.board and put it in the new spot
            checkerBoard.gameBoard[this.position[0]][this.position[1]] = 0;
            checkerBoard.gameBoard[tile.position[0]][tile.position[1]] = this.player;
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
            checkerBoard.gameBoard[this.position[0]][this.position[1]] = 0;
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


class AIObject {
    constructor() {
        this.playerNumber = 1;
        this.getMove = async (action="none") =>{
            const res = await axios.post('http://localhost:3000/', {
                action_str: action
              });
        }
    }
}


class Board {
    constructor(gameBoard, playerTurn, AI=false) {
        this.gameBoard = gameBoard;
        this.score = { player1: 0, player2: 0 };
        this.playerTurn = playerTurn;
        this.tileElements = $('div.tiles');
        this.dictionary = ["0vmin", "10vmin", "20vmin", "30vmin", "40vmin", "50vmin", "60vmin", "70vmin", "80vmin", "90vmin"]; 

        if (AI) {
            this.ai = new AIObject();

            if (playerTurn == this.ai.playerNumber) {
                const initialCPMove = await this.ai.getMove();
                console.log(initialCPMove);
            }
        }

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
                if (this.gameBoard[row][column] == 1) 
                    countPieces = this.renderPieces(1, row, column, countPieces)
                else if (this.gameBoard[row][column] == 2) 
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
        this.isValidPlaceToMove = (row, column) => {
            if (row < 0 || row > 7 || column < 0 || column > 7) return false;
            if (this.gameBoard[row][column] == 0) {
                return true;
            }
            return false;
        }
        this.changePlayerTurn = () => {
            if (this.playerTurn == 1) 
                this.playerTurn = 2;
            else 
                this.playerTurn = 1;
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
    }     
}

var checkerBoard = new Board(gameBoard, 1, true);
checkerBoard.initialize();
checkerBoard.getAndSetCPUMove();


// Handle events
$('.piece').on("click", function () {
    console.log("piece clicked");

    var selected;
    var isPlayersTurn = ($(this).parent().attr("class").split(' ')[0] == "player" + checkerBoard.playerTurn + "pieces");
    if (isPlayersTurn) {
      if (pieces[$(this).attr("id")].allowedToMove) {
        if ($(this).hasClass('selected')) selected = true;
        $('.piece').each(function (index) {
            $('.piece').eq(index).removeClass('selected')
        });
        if (!selected) {
          $(this).addClass('selected');
        }
      } 
    }
  });

$('.tile').on("click", function () {
    //make sure a piece is selected
    if ($('.selected').length != 0) {
        console.log("tile clicked");
        var tileId = $(this).attr("id").replace(/tile/, '');
        var tile = tiles[tileId];
        var pieceSelected = pieces[$('.selected').attr("id")];
   
        var possibleMove = tile.inRange(pieceSelected);
        if (possibleMove != 'wrong') {
            if (possibleMove == 'jump') {
                if (pieceSelected.opponentJump(tile)) {
                    pieceSelected.move(tile);
                    if (pieceSelected.canJumpAny()) {
                        pieceSelected.element.addClass('selected');
                        checkerBoard.continuousJump = true;
                    } else 
                        checkerBoard.changePlayerTurn();
                }
            } else if (possibleMove == 'regular' && !checkerBoard.jumpExists) {
                if (!pieceSelected.canJumpAny()) {
                    pieceSelected.move(tile);
                    checkerBoard.changePlayerTurn();
                } else 
                    console.log("You must jump when possible");
            }
        }
    }
});



