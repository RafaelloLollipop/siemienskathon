function Exception(message){
  this.message = message
}
Exception.prototype = new Error;
Exception.prototype.constructor = Exception;
