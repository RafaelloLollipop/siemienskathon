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
    div.setAttribute("data-id", room[0]);

    var ribbon = createRibbon();
    // div.appendChild(ribbon);

    var room_id = document.createElement("span");
    room_id.className = "room_id";
    room_id.inner_HTML = room[0];

    var room_name = document.createElement("div");
    room_name.className = "room_name";
    room_name.innerHTML = room[4];

    var owner = document.createElement("p");
    owner.innerHTML = "Room owner: " + room[1];
    owner.className = "owner";

    var players = document.createElement("p");
    players.innerHTML = "Players: " + room[2] + "/" + room[3];
    players.className = "players"

    div.appendChild(room_name);
    div.appendChild(owner);
    div.appendChild(players);

    div.addEventListener('click',joinRoom);

    document.getElementById("rooms").appendChild(div);
  }
}

function joinRoom(evt){
var id = this.getAttribute("room_name");
  if(document.getElementById("selected_room") !== null){
    document.getElementById("selected_room").removeAttribute('id');
  }
  this.id = "selected_room";
  var room_id = this.getAttribute("data-id");
  var player_name = window.localStorage.getItem("player_name");
  console.log("Room"+room_id);
  console.log("player"+player_name);

  connection.joinRoom(room_id,player_name);

  var preview = createPreview();
};

function roomUpdate(data){

    console.log("update");
    console.log(data);

    window.localStorage.setItem("game_script",data.game_script);

    var players_list = document.getElementById("players_list");
    players_list.innerHTML = data.players;

};

function setContainerDefaultContent(){
  var container = document.getElementById("container");

  var preview = elementWithId("div","room_preview");
  var welcome = elementWithId("h1","welcome");
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
};

function createTools(){
  var tools = document.getElementById("tools");
  var new_room = elementWithId("button","new_roow");
  var title = document.createElement("h1");
  new_room.addEventListener('click',function(){
    var room_name = prompt("Please enter your room name:","Magiczny Pokoj");
    var data = {"room_name": room_name};

    connection.sendData("newRoom", data);
  });
  new_room.innerHTML = "New Room";
  title.innerHTML = "Tools";


  tools.appendChild(title);
  tools.appendChild(new_room);
  return tools;
};


function createPreview(){

  var info = document.createElement("div");
  var game_name = document.createElement("h2");
  var description = document.createElement("p");
  var author = document.createElement("span");
  var version = document.createElement("span");
  var players = elementWithId("div","players_list");
  var chat = document.createElement("div");
  var id = document.createElement("span");

  var games_list = window.localStorage.getItem("game_list");

  games_list = JSON.parse(games_list);

  var updatePreviewInfo = function(){

      var select = document.getElementById("selectGame");
      for(var i=0; i < games_list.length; i++){
        game = games_list[i];
        if (games_list[i].name == select.value){
          id.innerHTML = "Room number " + document.getElementById("selected_room").getAttribute('data-id') + " currently playing:";
          id.id = "room_id_preview";
          description.innerHTML = game.description;
          author.innerHTML = "author: " + game.author + "<br />";
          version.innerHTML = "version: " + game.version + "<br /><br />";
        }
      }
      game_name.innerHTML = select.value;
  }

  var preview = document.getElementById("room_preview");
  preview.innerHTML = "";

  var ready_button = document.createElement("button");
  ready_button.innerHTML = "Ready!";
  ready_button.addEventListener('click',function(){
    var game_script = window.localStorage.getItem("game_script");
    loadScript(game_script,initializeGame);
    
  });

  var selectGame_button = document.createElement("button");
  selectGame_button.innerHTML = "Select game";
  selectGame_button.addEventListener('click',function(){
      var select = document.getElementById("selectGame");
      updatePreviewInfo();
  });

  var selectGame = elementWithId("select","selectGame");


  for(option_id in games_list){
    var option = document.createElement("option");
    option.innerHTML = games_list[option_id].name;
    selectGame.appendChild(option);
  }
  preview.appendChild(id);
    preview.appendChild(game_name);

  preview.appendChild(description);
  preview.appendChild(author);
  preview.appendChild(version);
  preview.appendChild(players);
  preview.appendChild(ready_button);
  preview.appendChild(selectGame);
  preview.appendChild(selectGame_button);

  updatePreviewInfo();

  return preview;
};

function elementWithId(type, id){
  var element = document.createElement(type);
  element.setAttribute("id",id);
  return element;
};
