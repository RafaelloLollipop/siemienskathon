var loadScript = function (url, callback){

    var script = document.createElement("script")

    script.type = "text/javascript";

    if (script.readyState){  //IE
        script.onreadystatechange = function(){
            if (script.readyState == "loaded" ||
                    script.readyState == "complete"){
                script.onreadystatechange = null;
                callback();
                connection.sendMessage("ready");
            }
        };
    } else {  //Others
        script.onload = function(){
            callback();
            connection.sendMessage("ready");
        };
    }

    script.src = url;
    document.getElementsByTagName("head")[0].appendChild(script);
}
