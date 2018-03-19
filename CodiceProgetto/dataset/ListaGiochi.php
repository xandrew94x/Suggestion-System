<?php
define('api_key','1C68C546AC3F6FE254F828B460786D99');
$first_gamer = 76561197960434622;

function estrai_giochi($steamid){
  $lista_giochi = [];
  $url_request=  file_get_contents("https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="
  .api_key."&steamid=".$steamid."&include_appinfo=1&include_played_free_games=1&format=json");
  $array_response = json_decode($url_request,true);
  $counter = 0;
  if($array_response['response']['game_count'] > 20){ //se l'utente ha piu di venti giochi in libreria
    for($i = 0; $i<sizeof($array_response['response']['games']); $i++){
      $nome_gioco = $array_response['response']['games'][$i]['name'];
      if($array_response['response']['games'][$i]['playtime_forever'] != 0){
        array_push($lista_giochi,$nome_gioco);
        $counter++;
      }
    }
  }
  echo "num giochi giocati: ".$counter."\n";
  return $lista_giochi;
}

function playersGamesList($numUtenti, $first_gamer){
  $counter = 0; //lo incrementiamo ogni volta che prediamo un utente dal profilo valido e pubblico
  $steamID = $first_gamer;
  $lista_completa = []; //lista di tutti gli utenti e i rispettivi giochi posseduti
  while($counter <= $numUtenti){
    $lista_giochi = [];
    //prendi il profilo con lo steamid
    //1- vedi se il profilo esiste 2-vedi se e pubblico
    //prendi i giochi e incrementa counter e lo steam id
    $url_request = file_get_contents("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=".api_key.
    "&steamids=".$steamID."&format=json");
    $profileInfo_array = json_decode($url_request,true);
    if(@$profileInfo_array['response']['players'][0] && $profileInfo_array['response']['players'][0]['communityvisibilitystate']==3){
      $lista_giochi = estrai_giochi($steamID); //lista dei giochi dell'utente n
      if(sizeof($lista_giochi) >= 20){ //se la lista di giochi continua ad avere dopo
        //i controlli del tempo di gioco ancora un limite minimo di 20 giochi
        $obj = (object) array('Utente'.$counter => $lista_giochi);
        array_push($lista_completa,$obj);
        echo $counter."\n";

        $nomefile = 'Utente'.$counter.".txt";
        $fp = fopen($nomefile,'w');
        salva_su_file($fp, $lista_giochi);
        $counter++; $steamID++;
      } else $steamID++;
    }
    else $steamID++;
  }
  return $lista_completa;
}

//salva su file di testo
function salva_su_file($fp, $array){
  for($i = 0; $i < sizeof($array); $i++){
    fwrite($fp, $array[$i]."\n");
  }
  fclose($fp);
}

$dati = playersGamesList(50, $first_gamer);
$fp = fopen('dati.json','w');
fwrite($fp, json_encode($dati));
fclose($fp);
?>
