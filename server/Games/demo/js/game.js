// DODAJ http://code.jquery.com/ui/1.8.21/jquery-ui.min.js DO KLIENTA

$( document ).ready(function(){
  $('div#container').html('<ul id="left" class="scale droppable"></ul><ul id="right" class="scale droppable"></ul><ul id="available" class="droppable"></ul><ul id="send"></ul>');
});


file = location.pathname.split( "/" ).pop();

link = document.createElement( "link" );
link.href = file.substr( 0, file.lastIndexOf( "." ) ) + ".css";
link.type = "text/css";
link.rel = "stylesheet";
link.media = "screen,print";

document.getElementsByTagName( "head" )[0].appendChild( link );


var Game = function() {
	var that = this;
  var id = window.localStorage.getItem("id");

  this.init = function (){



    this.weights = {"left" : [], "right" : [], "available" : []};
    this.data = {};
    this.player = {};
    this.players = [];
    this.foreign_propositions = [];
    this.my_propositions = [];
    this.weight_count = 0;
  };

  this.onStart = function(data){
    this.players = data["players"];
    this.weights["left"] = data["left"];
    this.weights["right"] = data["right"];
    this.weights["available"] = data["available"];
    this.my_propositions = data["to"];
    this.foreign_propositions = data["from"];

    for(i in players){
      this.players[i]['waitlist'] = {};	// initialize empty waitlist associated with each player
    }
  };

  this.dataHandler = function(data){
    switch(data.action){
      case "move_accepted":break;
      case "move_rejected":break;
      case "proposition_accepted":break;
      case "end":break;
    }
  };

  this.move_weight = function(from, to, weight){
    var data = {
      action: "move",
      from: from,
      to: to,
      weight: weight,
      id : id
    }
    window.connection.sendGameData(data);
  };

  this.make_proposition = function(from, to, weight){
    var data = {
      action: "proposition",
      from: from,
      to: to,
      weight: weight,
      id : id
    }
    window.connection.sendGameData(data);
  };

  this.remove_proposition = function(from,to,weight){
    for(i in this.my_propositions){
      var proposition = this.my_propositions[i];
      if(proposition["from"] == from &&
         proposition["to"] == to &&
         proposition["weight"] == weight){

      this.my_propositions.splice(i,1);
          var data = {
            action: "remove_proposition",
            from: from,
            to: to,
            weight: weight,
            id : id
          };
          window.connection.sendGameData(data);
      }
    }
  };

  this.updateUI = function(){
    var left = $("#left");
    var right = $("#right");
    var available = $("#available");

    left.empty();
    right.empty();
    available.empty();

    for(i in this.weights["left"]){
      var weight = (this.weights["left"][i]);
      $("#left").append(this.createWeightHTML(weight));
    }
    for(i in this.weights["right"]){
      var weight = (this.weights["left"][i]);
      $("#right").append(this.createWeightHTML(weight));
    }
    for(i in this.weights["available"]){
      var weight = (this.weights["left"][i]);
      $("#available").append(this.createWeightHTML(weight));
    }
  };

	this.reset = function(){
		$( ".droppable" ).sortable({
		  connectWith: ".droppable",

		  receive: function(event, ui) {
			to = this.id;
			from = ui.sender.attr('id');
			weight = ui.item.attr('data-weight');

			if (to == "send" && from == "send" && ui.item.hasClass('proposition')){

				$(ui.sender).sortable('cancel');
			}

			if (to == "send") {

				if ($(this).children().length > 1) {
					to = this.getAttribute('data-id');
					if ($('li[data-id='+to+']').children().hasClass('proposition')){
						newWeight = $('li[data-id='+to+']').children('.proposition');
						that.acceptProposalOfExchange(newWeight.attr('data-weight'), to, $('li[data-id='+to+']').children('.proposition'));
						ui.item.remove();
						that.scales[from].splice(that.scales[from].indexOf(parseInt(weight)),1);
						that.receive(newWeight.attr('data-weight'));
						alert("Exchange successful.");
					}
					else {
						$(ui.sender).sortable('cancel');
					}
				}

				else{
					to = this.getAttribute('data-id');
					that.scales[from].splice(that.scales[from].indexOf(parseInt(weight)),1);
					that.sendRequestToExchange(weight, to, ui.item);
					that.updateModel();
				}
			}
			else if (from == "send") {
				if (ui.item.hasClass('proposition')){
					$(ui.sender).sortable('cancel');
				}
				else{
					var player = ui.sender.attr('data-id');
					that.cancelExchange(weight, player);
					that.scales[to].push(parseInt(weight));
				}
			}
			else {
				that.scales[from].splice(that.scales[from].indexOf(parseInt(weight)),1);
				that.scales[to].push(parseInt(weight));
				console.log("Left " + that.scales.left);
				console.log("Right " + that.scales.right);
				console.log("Unused " + that.scales.available);
				that.updateModel();

			}
		  }
		}).disableSelection();
	};

  this.createWeightHTML = function(weight){
    switch(true){
      case (weight <=3): class_ = "small";break;
      case (weight >=6): class_ = "large";break;
      default : class_ = "medium";
    }
    var html = '<li class="weight '+class_+' ui-state-default" data-weight="' + weight + '">' + weight + ' kg</li>'
    return html;
  };



}

Game.prototype = clone(GamePrototype.prototype);
