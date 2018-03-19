
var search = "";
$("#myBtn").on("click", function() {
    search = $("#search-input").val();
    if(search === ""){
        document.getElementById("demo").innerHTML = '<div class="alert alert-danger"><strong>Danger! </strong>'+
            'Insert a valid input in the form "UtenteN" </div>'
    }else{
        document.getElementById("demo").innerHTML = "Suggested Games for: " + search;
        searchSuggestion(search);
    }
});
var items = [];
function searchSuggestion(search){
    var path_to_directory = 'https://api.myjson.com/bins/1ajyv1';
    document.getElementById("lista").innerHTML = "Request in progress...";
    $.getJSON( path_to_directory, function( data ) {
        items = [];
        $.each( data, function( key, val ) {
            if(key == search){
                $.each(val, function(chiave, valori){
                    items.push("<td>" + chiave + "</td><td>" + valori + "</td>");
                } );
            }
        });
        var elementi = "<table class='striped'><thead><tr><th>Game</th><th>Probability</th></tr></thead><tbody>";
        var counter = 5;
        for(var i = 0; i <= counter; i++){
            var elemento = "<tr>"+ items[i] +"</tr>"
            elementi += elemento;
        }
        elementi += "</tbody></table>";
        document.getElementById("lista").innerHTML = elementi;
        var button = document.querySelector("#myBtn2");
        button.style.display = "block";
    });
}

$("#myBtn2").on("click", function(){
    var button = document.querySelector("#myBtn2");
    button.style.display = "none";
    searchSuggestion2(search);
});

function searchSuggestion2(search){
        var elementi = "";
        for(var i = 6; i < items.length; i++){
            var elemento = "<tr>"+ items[i] +"</tr>"
            elementi += elemento;
        }
        $("tbody").append(elementi);
}





