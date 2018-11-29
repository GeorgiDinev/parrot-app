
var intervalId;
var timerPressedCount = 0;
function startScheduledPlaying(){

    var startTimerBtn = document.getElementById("scheduled-play-btn")
    startTimerBtn.style.backgroundColor = timerPressedCount % 2 == 0 ? GRAY_COLOR: BLUE_COLOR;
    startTimerBtn.innerHTML =  timerPressedCount % 2 == 0 ? "Stop Timer": "Start Timer";


    var timerDropDown = document.getElementById("time-picker");
    var timerValueMin = parseInt(timerDropDown.options[timerDropDown.selectedIndex].value);

    if(intervalId){
        clearInterval(intervalId);

        if(timerPressedCount % 2 != 0){// stop rec
        timerPressedCount++;
           return;
        }
    }

    intervalId = setInterval(playSound, timerValueMin * 60 * 1000);

    timerPressedCount++;
    function playSound(){
        var sound_index = Math.floor(Math.random() * sounds.length);
        var rnd_sound = sounds[sound_index];
        rnd_sound.play();
    }
}
