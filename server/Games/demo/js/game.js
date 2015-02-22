var Game = function(){
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
      case "move_accepted":this.move_accept_handler();break;
      case "move_rejected":this.move_rejected_handler();break;
      case "proposition_accepted":this.proposition_accepted_handler();break;
      case "end":this.end_handler();break;
    }
  };

  this.move_accept_handler = function(){};

  this.move_rejected_handler = function(data){
    var move_id = data.move_id;
    var move_data = this.moves.splice(move_id,1);

    var dest = $('#'+move_data[1]);
    var child_ind = dest.children.indexOf(move_data[2]);
    var child = dest.childNodes(child_ind);
    dest.removeChild(child);
    var source = $('#'+move_data[0]);
    source.appendChild(child);
  }

  this.move_weight = function(from, to, weight, move_id){
    var data = {
      action: "move",
      from: from,
      to: to,
      weight: weight,
      id : id,
      move_id : move_id
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
  }
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
  }

	this.reset = function(){
		$( ".droppable" ).sortable({
		  connectWith: ".droppable",

		  receive: function(event, ui) {
  			dest = this.id;
  			from = ui.sender.attr('id');
  			weight = ui.item.attr('data-weight');

        that.move_weight(from,dest,weight,this.moves.length);
        that.moves.push([from,dest,weight]);
		  }
		}).disableSelection();
	}

  this.createWeightHTML = function(weight){
    switch(true){
      case (weight <=3): class_ = "small";break;
      case (weight >=6): class_ = "large";break;
      default : class_ = "medium";
    }
    var html = '<li class="weight '+class_+' ui-state-default" data-weight="' + weight + '">' + weight + ' kg</li>'
    return html;
  }

}

Game.prototype = clone(GamePrototype.prototype);
