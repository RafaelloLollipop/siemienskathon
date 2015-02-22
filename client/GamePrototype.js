function GamePrototype(){};
GamePrototype.prototype.init = function (){
  throw new Exception("Init not implemented!");
};
GamePrototype.prototype.onStart = function (){
  throw new Exception("onStart not implemented!");
};
GamePrototype.prototype.dataHandler = function(){
  throw new Exception("dataHandler not implemented");
};

function clone (obj) {
  if (!obj) return;
  clone.prototype = obj;
  return new clone();
}
