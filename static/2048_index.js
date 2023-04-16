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
                        $(currentTile).css("background-color", "#FFFCEF").text(currentBoard[y - 1][x - 1]).css("color", "#000000");
                        break;
                    case 4:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#FFF3CD").text(currentBoard[y - 1][x - 1]).css({
                                                                                                                "color": "#000000",
                                                                                                                "font-size": "17px"
                                                                                                                });
                        break;
                    case 8:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#FFE69C").text(currentBoard[y - 1][x - 1]).css({
                                                                                                                "color": "#000000",
                                                                                                                "font-size": "18px"
                                                                                                                });
                        break;
                    case 16:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#FFDA6A").text(currentBoard[y - 1][x - 1]).css({
                                                                                                                "color": "#000000",
                                                                                                                "font-size": "19px"
                                                                                                                });
                        break;
                    case 32:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#FFCD39").text(currentBoard[y - 1][x - 1]).css({
                                                                                                                "color": "#000000",
                                                                                                                "font-size": "20px"
                                                                                                                });
                        break;
                    case 64:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#FFC107").text(currentBoard[y - 1][x - 1]).css({
                                                                                                                "color": "#000000",
                                                                                                                "font-size": "24px"
                                                                                                                });
                        break;
                    case 128:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#E8AF07").text(currentBoard[y - 1][x - 1]).css({
                                                                                                                "color": "#000000",
                                                                                                                "font-size": "28px"
                                                                                                                });
                        break;
                    case 256:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#CC9A06").text(currentBoard[y - 1][x - 1]).css({
                                                                                                                "color": "#000000",
                                                                                                                "font-size": "32px"
                                                                                                                });
                        break;
                    case 512:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#997404").text(currentBoard[y - 1][x - 1]).css({
                                                                                                                "color": "#000000",
                                                                                                                "font-size": "36px"
                                                                                                                });
                        break;
                    case 1024:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#664D03").text(currentBoard[y - 1][x - 1]).css({
                                                                                                                "color": "#FFFFFF",
                                                                                                                "font-size": "40px"
                                                                                                                });
                        break;
                    case 2048:
                        $(currentTile).empty();
                        $(currentTile).css("background-color", "#332701").text(currentBoard[y - 1][x - 1]).css({
                                                                                                                "color": "#FFFFFF",
                                                                                                                "font-size": "44px"
                                                                                                                });
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
                    backgroundUrl = "https://wallpapercave.com/wp/esSA024.jpg";
                    break;
                case 4:
                    backgroundUrl = "https://wallpapercrafter.com/desktop/164734-nature-Iceland-waterfall-landscape-water.jpg";
                    break;
                case 8:
                    backgroundUrl = "https://wallpapercave.com/wp/wp4287396.jpg";
                    break;
                case 16:
                    backgroundUrl = "../img/Polska.png";
                    break;
                case 32:
                    backgroundUrl = "https://wallpaperset.com/w/full/f/c/f/50692.jpg";
                    break;
                case 64:
                    backgroundUrl = "https://images.wallpaperscraft.com/image/single/field_meadow_grass_143602_1920x1080.jpg";
                    break;
                case 128:
                    backgroundUrl = "https://wallpapercave.com/wp/wp2249764.jpg";
                    break;
                case 256:
                    backgroundUrl = "https://wallpapercave.com/wp/wp1823655.jpg";
                    break;
                case 512:
                    backgroundUrl = "https://s27363.pcdn.co/wp-content/uploads/2022/03/Things-to-Do-in-Joshua-Tree.jpg.optimal.jpg";
                    break;
                case 1024:
                    backgroundUrl = "https://media.cntraveler.com/photos/54dd13cd72e816e54e62e61c/16:9/w_2560%2Cc_limit/tabernas-desert-spain-maphead.jpg";
                    break;
                case 2048:
                    backgroundUrl = "https://rare-gallery.com/uploads/posts/1240211-sahara-desert.jpg";
                    break;
                default:
                    backgroundUrl = "https://wallpapercave.com/wp/esSA024.jpg";
                    break;
            }

            $("body").css("background", "url(" + backgroundUrl + ")  no-repeat center center fixed");
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