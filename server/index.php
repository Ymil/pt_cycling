<?php 

use Symfony\Component\HttpFoundation\Response;
$app = new Silex\Application();




$app->put('/create_game/{player_name}/{n_players}', 
    function($player_name, $n_player) use($app){
        /*
         * Esta funcion es llamada cuando un usuario crea una sala
         * Recibe como parametros el nombre del jugador (player_name) y la
         * Cantidad de jugadores que tendra la sala (n_player)
         */
        // Query create game 
        $game_id = '';
        $response = Array('game_id' => game_id);
        return $app->json($response, 201);
});

$app->get('/status_game/{game_id}',
    function($game_id) use($app){
        /*
         * Esta función la llaman los usuarios que estas dentro de la sala
         * Para obtener información sobre el estado y el listado de jugadores
         * Esta mista funcion indica si la partida va a empezar respondiendo
         * La petición con http code 200
         * Recibe le parametro id de sala ($game_id)
         */
        // Query get status game
        $game_ready = True;
        $player_list = Array();
        $response = Array('player_list' => $player_list);
        if($game_ready){            
            return $app->json($response, 200);
        }else{
            return $app->json($response, 102);
        }
        
    });

$app->put('/start_game/{game_id}',
    function($game_id) use($app){
        /*
         * Esta funcion se lamma cuando el usuario master decide iniciar
         * La partida.
         * La solicitud a status indicara ready y iniciara la partida
         * Para todos los jugadores
         */
        // Query update status game_id ready
        return new Response(201, 'Starting');
    });

$app->put('/start_game_player/{game_id}/{player_name}/{datetime_sync}',
    function($game_id, $player_name, $datatime_sync) use($app){
        /* 
         * Esta funcion se llama cuando un jugador inicia su partida 
         * Envia el valor de game_id, su nombre y información sobre el sincro-
         * nismo.
         */
        // Query update status game_id ready
        return new Response(201, 'Starting');
    });

$app->put('/add_data_player/{game_id}/{player_name}/' +
    '{datatime_sync}/{player_distance}/'+
    +'{player_speed_max}/{player_speed_prom}',
    function($game_id, $player_name, 
        $datatime_sync, $player_dinstance, 
        $player_speed_max, $player_speed_prom) use($app){
        /*
         * Esta funcion se llama cuando un jugador desea agregar informacion de
         * su estado de avance
         * Se retorna un json con la informacion de avance del resto de jugadores
         */
        // Query insert data player
        // Query get last data others players
        $response = Array(
            Array('player_name' => 'X1', 'player_distance' => '', 
                'player_speed_max' => '', 'player_speed_prom'),
            Array('player_name' => 'X2', 'player_distance' => '',
                'player_speed_max' => '', 'player_speed_prom'),
            );
        return $app->json($response, 201);
    });

$app->run();
?>