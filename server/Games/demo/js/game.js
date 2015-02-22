/**
 * example game
 * 
 **/
var Game = function(){
	var that = this;
	
	this.data = {
		weights : [5, 5, 2, 1, 1],
		players : [
			{name:"Adamnie", id:1},
			{name:"Rosiu", id:2},
			{name:"Megs", id:3},
			{name:"Rafix", id:4} ]
		};
	this.scales = {"left" : [0], "right" : [0], "available" : [0]};
	
	this.player = {name:"Antek", id:8};
	this.players = this.data.players;

	for(var i = 0; i< that.players.length; i++){
		that.players[i]['waitlist'] = {};	// initialize empty waitlist associated with each player
	}
	
	
	this.sendRequestToExchange = function(weight, id, item){
		for(var i = 0; i< that.players.length; i++){
			if (that.players[i].id == id && $.isEmptyObject(that.players[i]['waitlist']) ) {
				that.players[i]['waitlist'] = {'weight':weight, 'init':that.player.id, 'uiHandler':item};	// send request, associate it with my id and remember item handler (!)
				alert("Waiting for acceptance from player " + that.players[i].name);
			}
		}
	}

	// my friend accepted my proposition, yay
	this.handleAcceptToExchange = function(weight, id, acceptedWeight){
		for(var i = 0; i < that.players.length; i++)
		{
			if (that.players[i].id == id && that.players[i].waitlist.weight == weight){
				that.players[i].waitlist.uiHandler.remove(); //delete from view, but SHOULD BE FROM THE MODEL!
				that.receive(acceptedWeight); // recieve new 
				that.waitlist = {}; // delete task from waitlist
				alert("Exchange with player " + that.players[i].name + " accepted!");
			}
		}
	}

	// lol nope, changed my mind
	this.cancelExchange = function(weight, id){
		for(var i = 0; i < that.players.length; i++)
		{
		  if(that.players[i].id == id && that.players[i].waitlist.weight == weight){
			that.players[i].waitlist = {};
			alert("You changed your mind.");
		  }
		}
	}
	

	// someone somwehere likes mey and wants to exchange
	this.handleProposalOfExchange = function(json){
		playerId = json.playerId;
		weight = json.weight;
		if (weight < 3){
			var class_ = "small";
		}
		else if (weight >=3 && weight < 6){
			var class_ = "medium";
		}
		else if (weight >=6 ){
			var class_ = "big";
		}
		$('li[data-id='+playerId+']').append('<li class="weight '+class_+' proposition ui-state-default" data-weight="' + weight + '">' + weight + ' kg</li>');
		for (var i=0; i<that.players.length; i++){
			if (that.players[i].id == playerId){
				that.players[i]['waitlist'] = {'weight':weight, 'init':playerId};
			}
		}
		
		//$( "li[data-id="+playerId+"]").sortable("disable");
	}
	

	// i hereby accept your generous offer
	this.acceptProposalOfExchange = function(weight, playerId, uiHandler){
		// TODO - SEND ACCEPTANCE TO SERVER
		if (that.players[playerId]['waitlist'].weight == weight && that.players[playerId]['waitlist'].init == playerId){
			uiHandler.remove();
			that.players[playerId]['waitlist'] = {};
		}
	}	
	
	this.receive = function(weight){
		if (weight < 3){
			var class_ = "small";
		}
		else if (weight >=3 && weight < 6){
			var class_ = "medium";
		}
		else if (weight >=6 ){
			var class_ = "big";
		}

		$('#available').append('<li class="weight '+class_+' ui-state-default" data-weight="' + weight + '">' + weight + ' kg</li>');
		that.scales.available.push(weight);
	}
	
	

	this.reset = function(){
		$('#available').empty();
		that.scales.left = [];
		that.scales.right = [];
		that.scales.available = that.data.weights;

		for(i = 0; i < that.data.weights.length; i++){
			weight = that.data.weights[i];
			if (weight < 3){
				var class_ = "small";
			}
			else if (weight >=3 && weight < 6){
				var class_ = "medium";
			}
			else if (weight >=6 ){
				var class_ = "big";
			}
			$('#available').append('<li class="weight '+class_+' ui-state-default" data-weight="' + that.data.weights[i] + '">' + that.data.weights[i] + ' kg</li>');
		}

		for(i = 0; i < that.data.players.length; i++){
			$('#send').append('<li class="player droppable ui-state-default" id="send" data-id="' + that.data.players[i].id + '">' + that.data.players[i].name + '</li>');
		}

		$( ".droppable" ).sortable({
		  connectWith: ".droppable",
		  receive: function(event, ui) {
			to = this.id;
			from = ui.sender.attr('id');
			weight = ui.item.attr('data-weight');
			console.log("FROM " + from + " TO: " + to);

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
	}

	this.updateModel = function(){
		if (that.scales.left.length > 0){
			var sumLeft = that.scales.left.reduce(function(a,b){return a+b;});
		}
		else{
			var sumLeft = 0;
		}
		if (that.scales.right.length > 0){
			var sumRight = that.scales.right.reduce(function(a,b){return a+b;});
		}
		else{
			var sumRight = 0;
		}
		if (sumLeft == sumRight && sumLeft != 0 && sumRight != 0 && that.scales.available.length == 0){
			alert('Balanced!');
		}
	}
	
}

Game.prototype = clone(GamePrototype.prototype);
//Game = new Game()
