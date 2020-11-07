
var ui = {};

//holds the state of the intial controls visibility
ui.intialControlsVisible = true;

//holds the setInterval handle for the robot flickering
ui.robotFlickeringHandle = 0;

//holds the current visible view
ui.currentView = "";


ui.startRobotFlickering = function() {
    ui.robotFlickeringHandle = setInterval(function() {
        $("#robot").toggleClass('robot');
    }, 500);
};

ui.stopRobotFlickering = function() {
    clearInterval(ui.robotFlickeringHandle);
};


ui.switchViewTo = function(turn) {

    //helper function for async calling
    function _switch(_turn) {
        ui.currentView = "#" + _turn;
        $(ui.currentView).fadeIn("fast");

        if(_turn === "ai")
            ui.startRobotFlickering();
    }

    if(ui.intialControlsVisible) {
        //if the game is just starting
        ui.intialControlsVisible = false;

        $('.intial').fadeOut({
            duration : "slow",
            done : function() {
                _switch(turn);
            }
        });
    }
    else {
        //if the game is in an intermediate state
        $(ui.currentView).fadeOut({
            duration: "fast",
            done: function() {
                _switch(turn);
            }
        });
    }
};


ui.insertAt = function(indx, symbol) {
    var board = $('.cell');
    var targetCell = $(board[indx]);

    if(!targetCell.hasClass('occupied')) {
        targetCell.html(symbol);
        targetCell.css({
            color : symbol == "X" ? "green" : "red"
        });
        targetCell.addClass('occupied');
    }
}
