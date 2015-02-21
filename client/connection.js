function Connection(game,server_address,server_port){
  this.game = game;
  this.websocket = null;
  this.server_uri = "ws://"+server_address+":"+server_port+"/game";
  this.init();
}

Connection.prototype.init = function(){
  console.log("Initializing connection");

  this.websocket = new WebSocket(this.server_uri);
  var _this = this;

  this.websocket.onopen = function (evt){_this.onOpen(evt);};
  this.websocket.onclose = function (evt){_this.onClose(evt);};
  this.websocket.onmessage = function (evt){_this.onMessage(evt);};
  this.websocket.onerror = function (evt){_this.onError(evt);};
};

Connection.prototype.onOpen = function(evt){
  this.sendMessage("connectToServer");
  console.log("Connecting to server...");
};

Connection.prototype.onClose = function(evt){
  this.sendMessage("disconnect");
  console.log("Connection closed...");
};

Connection.prototype.onMessage = function(evt){

  try{
    var data = evt.data;
    data = JSON.parse(data);
  }catch(e){
    console.log(e);
    return;
  }

  var message = data.message;

  switch(message){

    case "rooms" : window.showRooms();break;
    case "disconnect": this.game.onDisconnect();break;
    case "roomUpdate": this.game.onRoomUpdate();break;
    
    default : console.log("Unsupported message");
  }
};

Connection.prototype.sendMessage = function(message){
  var request = {
    message: message
  };
  request = JSON.stringify(request);
  this.websocket.send(request);
};

Connection.prototype.sendData = function(message, data){
  var request = {
    message: message,
    data : data
  };
  request = JSON.stringify(request);
  this.websocket.send(request);
};

Connection.prototype.selectGame = function(game_id){
  var data = {
    game_id : game_id
  };

  this.sendData(data);
};

Connection.prototype.joinRoom = function(room_id){
  var data = {
    room_id : room_id
  };
  this.sendData(data);
};

Connection.prototype.onError = function(evt){
  this.sendMessage("Error occured");
  console.log("Error occured...");
};

Connection.prototype.connectToRoom = function(room_id, player_name){
  var data = {
    name: player_name,
    room_id: room_id
  };
  this.sendData(data);
};
