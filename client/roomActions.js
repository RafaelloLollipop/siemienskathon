function createRibbon(){
  var ribbon = document.createElement("div");
  ribbon.className = "ribbon-wrapper-green";
  var innerRibbon = document.createElement("div");
  innerRibbon.className = "ribbon-green";
  innerRibbon.innerHTML = "No game assigned";
  ribbon.appendChild(innerRibbon);
  return ribbon;f
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

  var tools = createTools();
  container.appendChild(preview);
  container.appendChild(rooms);
  container.appendChild(tools);
  container.innerHTML += '<br style="clear: left;" />';
};

function createTools(){
  var tools = elementWithId("div","tools");
  var new_room = document.createElement("button");
  var title = document.createElement("h1");
  title.innerHTML = "Tools";
  new_room.innerHTML = "New Room";
  var data = {"player_id": window.localStorage.getItem("id")}
  new_room.addEventListener("click",function(){
    connection.sendData("newRoom", data);
  });
  tools.appendChild(title);
  tools.appendChild(new_room);
  return tools;
};

function createPreview(){
  var preview = document.getElementById("room_preview");
  preview.innerHTML = "";
  var info = document.createElement("div");
  var game_name = document.createElement("p");
  var players = elementWithId("div","players_list");
  var chat = document.createElement("div");

  var ready_button = document.createElement("button");
  ready_button.innerHTML = "Ready!"
  ready_button.addEventListener("click",function(){
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
