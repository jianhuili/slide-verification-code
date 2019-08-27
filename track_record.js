var sliderSelector = "#JDJRV-wrap-loginsubmit > div > div > div > div.JDJRV-slide-bg > div.JDJRV-slide-inner.JDJRV-slide-btn";

var siderElem = document.querySelector(sliderSelector);

var tracks = []
var tracks = [1,2,2,3,3,4,4,5,6,7,10,13,16,18,19,20,21,23,24,26,29,31,33,35,37,40,42,44,46,47,49,51,52,53,55,56,57,59,62,64,68,70,72,75,77,79,81,83,84,85,86,88,89,90,91,93,94,96,98,99,101,103,104,105,107,109,110,111,112,113,113,114,115,115,116,116,117,117,117,118,118,118,118,118,119,119,119,119,119]
var startX= siderElem.offsetLeft

var recordMoveTrack = function (siderElem, startX)
{
     tracks.push(siderElem.offsetLeft - startX);
}

var startX= siderElem.offsetLeft

//onmouseup /onmousedown
var timerFunc;
siderElem.addEventListener("onmousedown", function(){
    console.log("start to record");
   timerFunc = setInterval(()=> {recordMoveTrack(siderElem, startX) },10);
});

siderElem.addEventListener("onmouseup", function(){
    console.log("stop to record");
   clearInterval(timerFunc);
   console.log("tracks:" + JSON.stringify(tracks));
});

var tracks = []

var startX= siderElem.offsetLeft

var recordMoveTrack = function (siderElem, startX)
{
     tracks.push(siderElem.offsetLeft - startX);
}
var startX= siderElem.offsetLeft
var timerFunc = setInterval(()=> {recordMoveTrack(siderElem, startX) },50);
setTimeout(()=> { clearInterval(timerFunc); console.log("tracks:" + JSON.stringify(tracks));},10000)
