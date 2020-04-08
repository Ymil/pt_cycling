<?php 
require_once '../vendor/autoload.php';
include 'class_game.php';
include 'class_player.php';

use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Debug\ErrorHandler;
use Symfony\Component\Debug\ExceptionHandler;

// set the error handling
ini_set('display_errors', 1);
error_reporting(-1);
ErrorHandler::register();
if ('cli' !== php_sapi_name()) {
	ExceptionHandler::register();
}



$app = new Silex\Application();
$app['debug'] = true;


$app->error(function(\Exception $e) use ($app) {
	print $e->getMessage(); // Do something with $e
});

$app->register(new Silex\Provider\DoctrineServiceProvider(), array(
		'dbs.options' => array (
				'mysql_read' => array(
						'driver'    => 'pdo_mysql',
						'host'      => 'localhost',
						'dbname'    => 'pt_cycling',
						'user'      => 'pt_cycling',
						'password'  => '',
						'charset'   => 'utf8',
				),
		),
));

$app->get('/index', function(){
	return 'hola';
});

$app->put('/create_game/{player_name}/{n_players}/{distance}', 
		function($player_name, $n_players, $distance) use($app){
    	/*
    	 * Esta funcion es llamada cuando un usuario crea una sala
    	 * Recibe como parametros el nombre del jugador (player_name) y la
    	 * Cantidad de jugadores que tendra la sala (n_player)
    	 */
    	$game = New Game($app['db']);
    	$player = new Player($app['db'], $player_name);
    	$game->create($player, $n_players, $distance);    	
        $game_id = $game->get_id();  
        $response = Array('game_id' => $game->get_id());
        return $app->json($response, 201);
});

$app->put('/join_game/{game_id}/{player_name}',
		function($game_id, $player_name) use($app){
			/*
			 * Esta funcion es llamada cuando un usuario crea una sala
			 * Recibe como parametros el nombre del jugador (player_name) y la
			 * Cantidad de jugadores que tendra la sala (n_player)
			 */
			$game = New Game($app['db'], $game_id);
			if(!$game->exists()){
				return New Response('La sala no existe', 403);
			}
			$player = New Player($app['db'], $player_name);
			$result = $game->join_player($player);
			if($result == -1){
				return New Response('Ya ingresaste a la sala', 403);
			}else if(!$result){
				return New Response('La sala se encuentra llena', 403);
			}
			$response = Array('game_num_players' => $game.get_num_players(), "game_distance" => $game.get_distance());
			return $app->json($response, 200);  
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
    	$game = New Game($app['db'], $game_id);
    	if(!$game->exists()){
    		return New Response('La sala no existe', 403);
    	}
    	$game_status = $game->get_status();
    	$player_list = $game->get_players();
        $response = Array('game_status' => $game_status, 'game_players' => Array());        
        foreach ($game->get_players() as &$player_id){
        	if($player_id != $player->get_id()){
        		$other_player = New Player($app['db'], False, $player_id);
        		$other_player_name = $other_player->get_name();
        		$data = $other_player->get_data($game_id);
        		$response['game_players'][$player_id] = Array(
        				'player_name' => $other_player_name,
        				'player_distance' => 0.0,
        				'player_speed_prom' => 0.0,
        				'player_speed_max' => 0.0
        				);
        		if($data){
        			$response['game_players'][$player_id]['player_distance'] = $data['player_data_distance'];
        			$response['game_players'][$player_id]['player_speed_max'] = $data['player_data_speed_max'];
        		}
        	}
        }
        return $app->json($response, 200);        
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
    	$game = New Game($app['db'], $game_id);
    	if(!$game->exists()){
    		return New Response('La sala no existe', 403);
    	}
    	$game->start();    	
    	return new Response('Starting', 201);
    });

$app->put('/start_game_player/{game_id}/{player_name}/{datetime_sync}',
		function($game_id, $player_name, $datetime_sync) use($app){
        /* 
         * Esta funcion se llama cuando un jugador inicia su partida 
         * Envia el valor de game_id, su nombre y información sobre el sincro-
         * nismo.
         */
        // Query update status game_id ready
    	$game = New Game($app['db'], $game_id);
    	if(!$game->exists()){
    		return New Response('La sala no existe', 403);
    	}
    	if(!$game->get_status() == 4){
    		return New Response('', 403);
    	}
    	$player = New Player($app['db'], $player_name);    	
    	$game->player_start($player, $datetime_sync);
        return new Response('start', 201);
    });

$app->put('/finish_game_player/{game_id}/{player_name}/{datetime_sync}',
		function($game_id, $player_name, $datetime_sync) use($app){
			/*
			 * Esta funcion se llama cuando un jugador finaliza su partida
			 * Envia el valor de game_id, su nombre y información sobre el sincro-
			 * nismo.
			 */
			// Query update status game_id ready
			$game = New Game($app['db'], $game_id);
			if(!$game->exists()){
				return New Response('La sala no existe', 403);
			}
			if(!$game->get_status() == 4){
				return New Response('', 403);
			}
			$player = New Player($app['db'], $player_name);
			$game->player_finish($player, $datetime_sync);
			return new Response('end', 201);
		});

$app->put('/add_data_player/{game_id}/{player_name}/{player_datatime_sync}/{player_distance}/{player_speed_max}/{player_speed_prom}',
    function($game_id, $player_name, 
    		$player_datatime_sync, $player_distance, 
        	$player_speed_max, $player_speed_prom) use($app){
        /*
         * Esta funcion se llama cuando un jugador desea agregar informacion de
         * su estado de avance
         * Se retorna un json con la informacion de avance del resto de jugadores
         */
		$game = New Game($app['db'], $game_id);
        if(!$game->exists()){
        	return New Response('La sala no existe', 403);
        }
        if(!$game->get_status() == 5){
        	return New Response('', 403);
        }
        $player = New Player($app['db'], $player_name); 
        // Query insert data player
        // Query get last data others players
        
        $player->add_data($game_id, $player_datatime_sync, $player_distance, $player_speed_max);
        $response = Array();
        return $app->json($response, 201);
    });

$app->run();
?>