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
            await fetch('/exportrec', {method: 'POST', body:formdata, mode:'no-cors'});
        console.log('ccj');
        }
        }
    }
    }

// function sendData(data) {
//         console.log('fvfvfv');
//         // var records = document.getElementById('records');
//         var formSend = document.getElementById('file_send');
//         // var sent_text = document.getElementById('sent_text').value;
//         formSend.onclick = async (e) => {
//         e.preventDefault();
//         // console.log(records);
//         // var sent = document.getElementsByClassName(counter)[0];
//         // if(sent.style.display!='none'){var sent_id = sent.value;}
//         // console.log('sent_id',sent_id);
//         // console.log('sent_text',sent_text);
//         let formdata = new FormData();
//             formdata.append("file", data, "sample.wav");
//         //   formdata.append("sentence_id",sent_id);
//         //   formdata.append('sentence_error',sent_error_check);
//         //   formdata.append('sentence_text',sent_text);
//         let response = await fetch('expaudio', {
//             method: 'POST',
//             body:formdata
//         });
//         let result = await response.json();
//         if (result.message=='DATA SAVED SUCCESSFULLY'){
//         hide(counter);
//         counter = counter + 1;
//         show(counter);
//         // document.getElementById('sent_text').value = '';
//         // console.log(counter, '/', sent_list_length);
//         send_status.style.background='#008000';
//         send_status.innerHTML='Audio Sent';
//             let ffs = document.getElementById('file_send');
//         ffs.style.display='none';
//         }else{
//         send_status.style.background='#ff0000';
//         send_status.innerHTML=result.message;
//         }
//         status_off_timer = new Date().getTime();
//         t_status = setInterval(remove_status,10);
//         console.log('uploaded');
//     };
//     }


$('#recButton').addClass("notRec");
        recButton.onclick = e => {
        if($('#recButton').hasClass('notRec')){
          console.log('REcordingg startedd')
          // let ffs = document.getElementById('file_send');
            // ffs.style.display='inline-block';
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


// function visible_elements(){
//     record_right_bottom.style.visibility='visible';
//     data_img.style.visibility='visible';
//     record_left_bottom_bottom.style.visibility='visible';
//     mic.style.visibility='visible';
//     }


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
