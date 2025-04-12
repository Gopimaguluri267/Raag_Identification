var counter = 0;
var running = 0;
var startTime;
var updatedTime;
var difference;
var t_interval;
var t_status;
var status_off_timer;
var timerDisplay = document.querySelector('.timer');

navigator.mediaDevices.getUserMedia({audio:true}).then(stream => {handlerFunction(stream)})

function handlerFunction(stream) {
    rec = new MediaRecorder(stream);
    rec.ondataavailable = e => {
        audioChunks.push(e.data);
        if (rec.state == "inactive"){
        let blob = new Blob(audioChunks,{type:'audio/wav'});

        console.log(rec);

        recordedAudio.src = URL.createObjectURL(blob);
        recordedAudio.controls=true;
        recordedAudio.autoplay=false;
        // sendData(blob)
        var formSend = document.getElementById('file_send');
        formSend.onclick = async (e) => {
            e.preventDefault();
            let formdata = new FormData();
            formdata.append("file", blob, "sample.wav");
            try {
                const response = await fetch('http://localhost:8000/exportrec', {
                    method: 'POST',
                    body: formdata
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                console.log('File uploaded successfully');
            } catch (error) {
                console.error('Error uploading file:', error);
            }
        }
        }
    }
    }


$('#recButton').addClass("notRec");
        recButton.onclick = e => {
        if($('#recButton').hasClass('notRec')){
          console.log('REcordingg startedd')
          audioChunks = [];
          rec.start();
          startTimer();
          $('#recButton').removeClass("notRec");
		      $('#recButton').addClass("Rec");
          $('#stopButton').removeClass("recStop");
          $('#stopButton').addClass("recRun");
		}
    }


$('#stopButton').addClass("recRun");
stopButton.onclick = e =>{
console.log("Recording Stopped");
stopTimer();
rec.stop();
console.log(difference);
$('#recButton').removeClass("Rec");
$('#recButton').addClass("notRec");
$('#stopButton').removeClass("recRun");
$('#stopButton').addClass("recStop");
}


function getShowTime(){
    updatedTime = new Date().getTime();
    difference =  updatedTime - startTime;
    var minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((difference % (1000 * 60)) / 1000);
    var milliseconds = Math.floor(difference % (1000 ));
    if (minutes>=2){
            rec.stop();
            stopTimer();
            alert('Time exceeded max range of '+minutes+'min.');   
            }
    minutes = (minutes < 10) ? "0" + minutes : minutes;
    seconds = (seconds < 10) ? "0" + seconds : seconds;
    milliseconds = (milliseconds < 100) ? (milliseconds < 10) ? "00" + milliseconds : "0" + milliseconds : milliseconds;
    timerDisplay.innerHTML =  minutes + ':' + seconds + ':' + milliseconds;   
    }


function remove_status(){
    updatedTime = new Date().getTime();    
        var status_difference = updatedTime - status_off_timer;
        var status_seconds = Math.floor((status_difference % (1000 * 60)) / 1000);
        if(status_seconds>=2){
            send_status.style.background='#ffffff';
            clearInterval(t_status);
        }
    }


function startTimer(){
    startTime = new Date().getTime();
    t_interval = setInterval(getShowTime, 100);
    }

    
function stopTimer(){
clearInterval(t_interval);
};