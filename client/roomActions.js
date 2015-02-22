function createRibbon(){
  var ribbon = document.createElement("div");
  ribbon.className = "ribbon-wrapper-green";
  var innerRibbon = document.createElement("div");
  innerRibbon.className = "ribbon-green";
  innerRibbon.innerHTML = "No game assigned";
  ribbon.appendChild(innerRibbon);
  return ribbon;
}

function showRooms(rooms){

  if(!document.getElementById("rooms")){
    var rooms_div = elementWithId("rooms");
    document.getElementById("container").appendChild(rooms_div);
  }

  document.getElementById("rooms").innerHTML = "";

  for(id in rooms){
    room = rooms[id];

    var div = elementWithId("div",room[0]);
    div.className = "room";

    var ribbon = createRibbon();
    // div.appendChild(ribbon);

    var room_id = document.createElement("p");
    room_id.className = "room_id";
    room_id.innerHTML = "Room id: " + room[0];

    var owner = document.createElement("p");
    owner.innerHTML = "Room owner: " + room[1];
    owner.className = "owner";

    var players = document.createElement("p");
    players.innerHTML = "Players: " + room[2] + "/" + room[3];
    players.className = "players"

    div.appendChild(room_id);
    div.appendChild(owner);
    div.appendChild(players);

    div.addEventListener('click',joinRoom)

    document.getElementById("rooms").appendChild(div);
  }
}

function joinRoom(evt){
  var id = this.getAttribute("room_id");
  connection.joinRoom(id);
  var preview = createPreview();

};

function roomUpdate(data){
    console.log("update");

    window.localStorage.setItem("game_script", data.game_script);

    var players_list = document.getElementById("players_list");
    players_list.innerHTML = data.players;
};

function setContainerDefaultContent(){
  var container = document.getElementById("container");

  var preview = elementWithId("div","room_preview");
  var welcome = elementWithId("h2","welcome");
  welcome.innerHTML = "Welcome!"
  var info = elementWithId("p","info");
  info.innerHTML += 'Click on any of the boxes on the left '
  + ' to see a game preview. ' + 'To join game click "ready" button'
  + ' in the preview box of the game you want to play';
  preview.appendChild(welcome);
  preview.appendChild(info);


  var rooms = elementWithId("div","rooms");

  var tools = elementWithId("div","tools");

  container.appendChild(preview);
  container.appendChild(rooms);
  container.appendChild(tools);
  container.innerHTML += '<br style="clear: left;" />';

  createTools();

  console.log(document.getElementById("new_room"));
};

function createTools(container){
  var tools = document.getElementById("tools");
  var new_room_button = elementWithId("button","new_room");
  var title = document.createElement("h1");

  title.innerHTML = "Tools";

  new_room_button.addEventListener('click', function(){
    var room_name = prompt("Type your room name:","defaultName"+Math.floor(Math.random()*100));
    var data = {"player_id": window.localStorage.getItem("id"),"room_name":room_name};

    connection.sendData("newRoom", data);
  });
  new_room_button.innerHTML = "New Room";

  tools.appendChild(title);
  tools.appendChild(new_room_button);
};

function createPreview(){
  var preview = document.getElementById("room_preview");
  preview.innerHTML = "";
  var info = document.createElement("div");
  var game_name = document.createElement("p");
  var players = elementWithId("div","players_list");
  var chat = document.createElement("div");

  var ready_button = document.createElement("button");
  ready_button.innerHTML = "Ready!";
  ready_button.addEventListener('click',function(){
    console.log("chuj");
    console.log(connection);
    connection.sendMessage("ready");
    var game_script = window.localStorage.getItem("game_script");
    loadScript(game_script,initializeGame);
  });

  var selectGame_button = document.createElement("button");
  selectGame_button.innerHTML = "Select game";
  selectGame_button.addEventListener('click',function(){
      var select = document.getElementById("selectGame");
      connection.selectGame(select.value);
  });


  var selectGame = elementWithId("select","selectGame");
  var games_list = window.localStorage.getItem("game_list");

  games_list = JSON.parse(games_list);

  for(option_id in games_list){
    var option = document.createElement("option");
    option.innerHTML = games_list[option_id];
    selectGame.appendChild(option);
  }

  preview.appendChild(game_name);
  preview.appendChild(players);
  preview.appendChild(ready_button);
  preview.appendChild(selectGame);
  preview.appendChild(selectGame_button);

  return preview;
};

function elementWithId(type, id){
  var element = document.createElement(type);
  element.setAttribute("id",id);
  return element;
};
