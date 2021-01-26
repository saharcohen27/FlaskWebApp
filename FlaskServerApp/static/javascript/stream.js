const videoElem = document.getElementById("video");

var socket = io();
socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
});

socket.on('pong', (screen) => {
    videoElem.srcObject = screen;
});

async function startCapture(displayMediaOptions) {
    let captureStream = null;
    try {
      screen = await navigator.mediaDevices.getDisplayMedia(displayMediaOptions);
      ok = true
      while(ok)
        if (screen){
            videoElem.srcObject = screen;
            socket.emit('screenCapture', screen);
            ok = false
        }
    } catch (err) {
      console.error("Error: " + err);
    }
}