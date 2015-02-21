
var server_address = "192.168.0.10:8888";
var server_uri = "ws://"+server_address+"/game";
var websocket;

function init(){
  console.log("Initializing webscoket");
  websocket = new WebSocket(server_uri);

  websocket.onopen = function (evt){onOpen(evt);};
  websocket.onclose = function (evt){onClose(evt);};
  websocket.onmessage = function (evt){onMessage(evt);};
  websocket.onerror = function (evt){onError(evt);};
}

function onOpen(evt){
  sendMessage("connectToServer");
  console.log("Connecting to server...");
}
function onClose(evt){
  sendMessage("disconnect");
  console.log("Connection closed...");
}

function onMessage(evt){

  try{
    var data = evt.data;
    data = JSON.parse(data);
  }catch(e){
    console.log(e);
  }

  var message = data.message;

  switch(message){
    case "rooms" : console.log("Received room list"); break;
    case "disconnect": console.log("Server shuts down");break;
    default: console.log("Unsupported message");
  }
}

function sendMessage(message){
  var request = {
    message: message
  };
  request = JSON.stringify(request);
  websocket.send(request);
}

function onError(evt){
  sendMessage("Error occured");
  console.log("Error occured...");
}

function connectToRoom(room_id, player_name){
  var request = {
    message: "connectToRoom",
    name: player_name,
    room_id: room_id
  };
  request = JSON.stringify(request);
  websocket.send(request);
}

window.addEventListener("load", init, false);
