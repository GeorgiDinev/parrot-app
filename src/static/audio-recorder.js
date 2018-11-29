var sounds = [];


var recordingBtn = document.getElementById("start-rec-btn");
recordingBtn.innerHTML= "Start Recording";
(function getParrotSounds(){
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            var parrotSounds = JSON.parse(xhr.response);

            for (index in parrotSounds){
                sounds.push(new Audio("/sounds/" + parrotSounds[index]));
            }
        }
    }
    xhr.open('GET', SOUND_NAMES_URL, true);
    xhr.send(null);
})();


var contextClass = (window.AudioContext ||
        window.webkitAudioContext ||
        window.mozAudioContext ||
        window.oAudioContext ||
        window.msAudioContext);
var gumStream;
var input;
var rec;
var isRecordingAllowed = true;

var audioContext = new contextClass();

var recordButton = document.getElementById("start-rec-btn");
recordButton.addEventListener("click", startRecording);

var isInitialized = false;
var stopRecordingIntervalId;

var startRecordingPressedCount = 0;
function startRecording() {
    recordingBtn.style.backgroundColor = startRecordingPressedCount % 2 == 0 ? GRAY_COLOR: BLUE_COLOR;
    recordButton.innerHTML = startRecordingPressedCount % 2 == 0 ? "Stop Recording": "Start Recording";

    if(startRecordingPressedCount % 2 != 0){
          clearInterval(stopRecordingIntervalId);
          startRecordingPressedCount++;
          return;
      }

    var constraints = { audio: true, video:false }

    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

        gumStream = stream;
        input = audioContext.createMediaStreamSource(stream);

        rec = new Recorder(input,{numChannels:1});
        rec.record();

        console.log("Recording started");

    }).catch(function(err) {
        console.log("GetUserMedia failed.")
    });

        if(stopRecordingIntervalId){
            clearInterval(stopRecordingIntervalId);
        }

        stopRecordingIntervalId = setInterval(stopRecording, 3000);

        startRecordingPressedCount++;
}


function stopRecording() {
    if(!isRecordingAllowed){return;}
    console.log("Recording  stopped.")
    rec.stop();

    rec.exportWAV(uploadRecording);
    rec.clear();
    rec.record();
}

function uploadRecording(blob){
    var filename = new Date().toISOString(); //filename to send to server without extension
    //upload link
    var upload = document.createElement('a');
    upload.href= "#";
    upload.innerHTML = "Upload";

    that = this;
    upload.addEventListener("click", function(event){
          var xhr=new XMLHttpRequest();

          xhr.onload=function(e) {
              if(this.readyState === 4) {
                  var isScreaming = JSON.parse(e.target.response)["is_parrot_screaming"];

                  console.log("Server returned: ", isScreaming);

                  if(isScreaming){
                    that.isRecordingAllowed = false
                    document.getElementById("result-btn").style.background='#ff0000';
                    rec.stop();
                    rec.clear();

                    var sound_index = Math.floor(Math.random() * sounds.length);
                    var rnd_sound = sounds[sound_index];
                    if(rnd_sound == undefined){
                       setTimeout(function() {
    that.isRecordingAllowed = true;
}, Math.floor(20 * 1000)); //
                       return;
                    }
                    rnd_sound.play();

                   //timeoutDurationMillis = rnd_sou;

                   console.log("TImeoutDur millis: " + timeoutDurationMillis)
                   setTimeout(function()
                   {
                   that.isRecordingAllowed = true;
                   }, Math.floor(timeoutDurationMillis * 1000)); //

                  }else{
                    document.getElementById("result-btn").style.background='#00fa00';
                  }
              }
          };
          var fd=new FormData();
          fd.append("audio_data",blob, filename);
          xhr.open("POST", UPLOAD_ROUTE,true);
          xhr.send(fd);
          console.log(blob)
    })
     upload.click();
}
