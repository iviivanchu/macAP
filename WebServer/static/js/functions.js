/*

    * Program for interact with server and informs if user is connected or disconnected.
    * Comunication system
    * Developed by Ivan Chamero and Manuel Angel Roman  

*/



/*

-----
Code
-----

*/


function checkChanges(){
  /*
  It sends AJAX requests to the server to find out about 
  connected and disconnected users.
  */

    var request;
    var msg;
    var url = "/api/changes";

    request=new XMLHttpRequest();
    request.onreadystatechange=function() {
      if (request.readyState==4 && request.status==200) {
           msg = JSON.parse(request.responseText);
           document.getElementById("newchange").innerHTML = msg["msg"];
           setTimeout( () => { window.location.href = "/admin"; }, 2000);
      }
    }
    request.open("GET", url, true);
    request.send();
}
