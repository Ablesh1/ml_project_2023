$(document).ready(function(){
    // Initial gameboard
    var currentBoard = [[0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]];
    var seed = true


    function refreshBoard(requestJson){
        // Send request
        somePackage.send(requestJson)

        // Receive response
        somePackage.connect()

        console.log(currentBoard);

        // Set colors
        for (var y = 1; y <= 4; y++){
            for (var x = 1; x <= 4; x++){
                var currentTile = '#tile-map > div:nth-child(' + y + ') > div:nth-child(' + x + ') > div:nth-child(1)';
                // Of tiles and text
                switch (currentBoard[y - 1][x - 1]){
                    case 2:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#368ead").text(currentBoard[y - 1][x - 1]).css("color", "#000000");
                        break;
                    case 4:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#c0ecfc").text(currentBoard[y - 1][x - 1]).css("color", "#000000");
                        break;
                    case 8:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#87ffd3").text(currentBoard[y - 1][x - 1]).css("color", "#000000");
                        break;
                    case 16:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#00FF7F").text(currentBoard[y - 1][x - 1]).css("color", "#000000");
                        break;
                    case 32:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#00753a").text(currentBoard[y - 1][x - 1]).css("color", "#000000");
                        break;
                    case 64:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#e5ff3b").text(currentBoard[y - 1][x - 1]).css("color", "#000000");
                        break;
                    case 128:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#f7ba02").text(currentBoard[y - 1][x - 1]).css("color", "#000000");
                        break;
                    case 256:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#b57602").text(currentBoard[y - 1][x - 1]).css("color", "#000000");
                        break;
                    case 512:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#fa7a02").text(currentBoard[y - 1][x - 1]).css("color", "#000000");
                        break;
                    case 1024:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#fa2b02").text(currentBoard[y - 1][x - 1]).css("color", "#FFFFFF");
                        break;
                    case 2048:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#4d0d00").text(currentBoard[y - 1][x - 1]).css("color", "#FFFFFF");
                        break;
                    default:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#FFFFFF");
                }
            }
        }
    }


    // Websocket management
    var somePackage = {};
    somePackage.connect = function()  {
        var ws = new WebSocket('ws://localhost:8765');
        ws.onopen = function() {
            console.log('ws connected');
            somePackage.ws = ws;
        };
        ws.onerror = function() {
            console.log('ws error');
        };
        ws.onclose = function() {
            console.log('ws closed');
        };
        ws.onmessage = function(msgevent) {
            var msg = JSON.parse(msgevent.data);
            console.log('in :', msg);

            // Read new board
            currentBoard = msg.board;

            // Check status and close connection if lost or won
            if (msg.statusCode === 1){
                $("#message").text("YOU WON! CONGRATS!").css("color", "#332701");
                ws.onclose()
            } else if (msg.statusCode === 255) {
                $("#message").text("YOU LOST! UNLUCKY!").css("color", "#FF0000");
                ws.onclose()
            }

            var backgroundUrl;
            // Set color of background and title
            switch (msg.topValue) {
                case 2:
                    backgroundUrl = "../img/january_pixel.png";
                    break;
                case 4:
                    backgroundUrl = "../img/february_pixel.png";
                    break;
                case 8:
                    backgroundUrl = "../img/march_pixel.png";
                    break;
                case 16:
                    backgroundUrl = "../img/april_pixel.png";
                    break;
                case 32:
                    backgroundUrl = "../img/may_pixel.png";
                    break;
                case 64:
                    backgroundUrl = "../img/june_pixel.png";
                    break;
                case 128:
                    backgroundUrl = "../img/july_pixel.png";
                    break;
                case 256:
                    backgroundUrl = "../img/august_pixel.png";
                    break;
                case 512:
                    backgroundUrl = "../img/september_pixel.png";
                    break;
                case 1024:
                    backgroundUrl = "../img/october_pixel.png";
                    break;
                case 2048:
                    backgroundUrl = "../img/november_pixel.png";
                    break;
                default:
                    backgroundUrl = "../img/january_pixel.png";
                    break;
            }


            $(".image").css("background-image", "url(" + backgroundUrl + ")");
            $("h1").css("color", "#000000");
            $("p").css("color", "#000000");
        };
    };


    somePackage.send = function(msg) {
        if (!this.ws) {
            console.log('no connection');
            return;
        }
        console.log('out:', msg)
        this.ws.send(window.JSON.stringify(msg));
    };


    // Communication with game logic
    somePackage.connect();

    // For arrows and wsad
    $(this).on('keydown', function(event) {
        var request = {};
        request.board = currentBoard;
        request.seed = seed;

        seed = false;

        // Left --- arrow
        if (event.keyCode === 37 || event.keyCode === 65) {
            request.direction = "a";
            refreshBoard(request);
        } // Up
        else if (event.keyCode === 38 || event.keyCode === 87) {
            request.direction = "w";
            refreshBoard(request);
        } // Right
        else if (event.keyCode === 39 || event.keyCode === 68) {
            request.direction = "d";
            refreshBoard(request);
        } // Down
        else if (event.keyCode === 40 || event.keyCode === 83) {
            request.direction = "s";
            refreshBoard(request);
        }
    })

    // Send fake request on key up to refresh the board
    $(this).on('keyup', function (_event){
        var request = {};
        request.board = currentBoard;
        request.direction = "e";
        request.seed = false;

        refreshBoard(request);
    })
});