
var initial_board_state = [ 2,2,2,2, // (10,0) (30,0) (50,0) (70,0)
                          + 2,2,2,2, // (0,10) (20,10) (40,10) (60,10)
                          + 2,2,2,2, // (10,20) (30,20) (50,20) (70,20)
                          + 0,0,0,0, // (0,30) (20,30) (40,30) (60,30)
                          + 0,0,0,0,
                          + 1,1,1,1,
                          + 1,1,1,1,
                          + 1,1,1,1 ];

var tiles = [];
var pieces = [];


class Tile {
    constructor(element, position, piece=null) {
        this.element = element;
        this.position = position;
        this.piece = piece; // use this

        this.inRange = (piece) => {
            for (let k of pieces)
                if (k.position == this.position && k.position == this.position)
                    return 'wrong'; // same spot
            if (!piece.king && piece.player == 2 && this.position < piece.position)
                return 'wrong';
            if (!piece.king && piece.player == 1 && this.position > piece.position)
                return 'wrong';
            if (dist(this.position, this.position, piece.position, piece.position) == Math.sqrt(2))
                return 'regular'; // regular move
            else if (dist(this.position, this.position, piece.position, piece.position) == 2 * Math.sqrt(2))
                return 'jump'; // jump move
        };
    }
}

class GameBoard {
    constructor(initial_board_state) {
        this.board_dimensions = ["0vmin", "10vmin", "20vmin", "30vmin", "40vmin", "50vmin", "60vmin", "70vmin", "80vmin", "90vmin"];
        this.board_state = initial_board_state;
        this.score = { player1: 0, player2: 0 };
        this.tileElements = $('div.tiles');
        this.player_pieces = {
            "pieces": $('pieces'),
            "player1pieces": $('div.player1pieces'),
            "player2pieces": $('div.player2pieces')
        }
        this.player_turn;
        this.tiles = [];
        this.pieces = [];

        this.initialize = (player_turn) => {
            this.instantiateTiles();
            // this.initializePieces();

            this.tiles = tiles;
        }
        this.initializePieces = () => {
            
        }
        this.instantiateTiles = () => {
            let id_pointer_left = 0,
                id_pointer_right = 4;

            this.createTiles = (left, top, count) => {
                this.tileElements.append("<div class='tile' id='tile" + count + "' style='top:" + top + ";left:" + left + ";'></div>");
                tiles[count] = new Tile($("#tile" + count), count);
            }
            for (let i = 0; i < 8; i++) {
                if (i % 2 == 0) {
                    this.createTiles(this.board_dimensions[i], this.board_dimensions[1], id_pointer_right);
                    this.createTiles(this.board_dimensions[i], this.board_dimensions[3], id_pointer_right+8);
                    this.createTiles(this.board_dimensions[i], this.board_dimensions[5], id_pointer_right+16);
                    this.createTiles(this.board_dimensions[i], this.board_dimensions[7], id_pointer_right+24);
                    id_pointer_right++;
                }
                else if (i % 2 == 1) {
                    this.createTiles(this.board_dimensions[i], this.board_dimensions[0], id_pointer_left);
                    this.createTiles(this.board_dimensions[i], this.board_dimensions[2], id_pointer_left+8);
                    this.createTiles(this.board_dimensions[i], this.board_dimensions[4], id_pointer_left+16);
                    this.createTiles(this.board_dimensions[i], this.board_dimensions[6], id_pointer_left+24);
                    id_pointer_left++;
                }
            }
        }
    }
}

var gb = new GameBoard(initial_board_state);
gb.instantiateTiles()
console.log(gb);