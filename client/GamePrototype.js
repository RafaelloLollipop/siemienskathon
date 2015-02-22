function GamePrototype(){};
GamePrototype.prototype.init = function (){
  throw new Exception("Init not implemented!");
};
GamePrototype.prototype.onStart = function (){
  throw new Exception("onStart not implemented!");
};
GamePrototype.prototype.finish = function(){
  throw new Exception("Finish not implemented!");
};
GamePrototype.prototype.onConnectionClose = function (){
  throw new Exception("onConnectionClose not implemented!");
};
GamePrototype.prototype.disconnect = function(){
  throw new Exception("Disconnect not implemented!");
};
GamePrototype.prototype.onRoomUpdate = function(){
  throw new Exception("OnRoomUpdate not implemented");
}
GamePrototype.prototype.dataHandler = function(){
  throw new Exception("dataHandler not implemented");
}

function clone (obj) {
  if (!obj) return;
  clone.prototype = obj;
  return new clone();
}
