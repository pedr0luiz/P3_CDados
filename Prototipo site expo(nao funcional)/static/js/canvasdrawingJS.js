document.addEventListener('DOMContentLoaded',function(){
// ------------------------------------------------------------------- //

  // Drawing App Vanilla JS using Canvas HTML Graphic Element
  var Canvas = document.querySelector('#canvasDraw')
  var contexto = Canvas.getContext('2d')
  Canvas.width = 1000;
  Canvas.height = 660;
  var radius = 4;
  var dragging = false;
  contexto.lineWidth = radius*2
  // Dummy Canvas for white background
  var dummyCanvas = document.createElement("canvas")
  dummyCanvas.width = Canvas.width
  dummyCanvas.height = Canvas.height
  var dummyContexto = dummyCanvas.getContext('2d')
  dummyContexto.fillStyle = 'white';
  dummyContexto.fillRect(0, 0, Canvas.width, Canvas.height);
  // Drawing Functions and EventListeners
  var putPoint = function(e){
  if(dragging){
    var x = e.clientX - 192;
    var y = e.clientY - 80
    console.log("X:"+ x)
    console.log("Y:"+ y)
    contexto.lineTo(x,y);
    contexto.stroke()
    contexto.beginPath()
    contexto.arc(x,y,radius,0,Math.PI*2);
    contexto.fill();
    contexto.beginPath()
    contexto.moveTo(x,y);
   }
  }
  var engage = function(e){
    dragging = true;
    putPoint(e);
  }
  var disengage = function(){
    dragging = false;
    contexto.beginPath()
  }
  Canvas.addEventListener('mousedown',engage);
  Canvas.addEventListener('mousemove',putPoint);
  Canvas.addEventListener('mouseup',disengage);
// ------------------------------------------------------------------- //

  // Send info to Flask when user manually submit
  let placeHolder = document.querySelector(".InputHolder")
  let Submit = document.querySelector(".botaoSubmit")
  Submit.addEventListener('click',function(){
    dummyContexto.drawImage(Canvas, 0, 0);
    var data = dummyCanvas.toDataURL()
    placeHolder.value = data
  })

  // Timer, when runs out automatically submit
  function countdown() {
      seconds = document.querySelector('.countdownNumber').innerHTML;
      seconds = parseInt(seconds);
      if (seconds == 1) {
        temp = document.querySelector('.countdownNumber');
        Submit.click()
        return;
      }
      seconds--;
      temp = document.querySelector('.countdownNumber');
      temp.innerHTML = seconds;
      timeout = setTimeout(countdown, 1000);
    }
    countdown();

})
