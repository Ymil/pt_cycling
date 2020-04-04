<?php 
class Game_player_data{
	function player_data_create($player){
		$query = $this->db->prepare("SELECT * FROM game_player_data
			WHERE game_player_data_game_id = ? and game_player_data_player_id = ?");
		$query->bindValue(1, $this->game_id);
		$query->bindValue(2, $player->get_id());
		$query->execute();
		$result = $query->fetch();
		if(!$result){
			$this->db->insert('game_player_data', 
					Array(
					'game_player_data_player_id' => $player->get_id(),
							'game_player_data_game_id' => $this->game_id
				));
		}
	}
	
	function player_data_set_start($player, $date){
		$this->db->update('game_player_data', 
				Array('game_player_data_start_date' => $date),
				Array('game_player_data_game_id' => $this->game_id, 
						'game_player_data_player_id' => $player->get_id()));		
	}
	
	function player_data_set_end($player, $date){
		$this->db->update('game_player_data',
				Array('game_player_data_end_date' => $date),
				Array('game_player_data_game_id' => $this->game_id,
						'game_player_data_player_id' => $player->get_id()));
	}
	
	function player_data_start_all(){
		/*
		 * Esta funcion se llama para verificar si todos los jugadores iniciaron la partida
		 */
		$query = $this->db->prepare("SELECT COUNT(*) as COUNT FROM game_player_data 
			WHERE game_player_data_game_id = ? and game_player_data_start_date > 0");
		$query->bindValue(1, $this->game_id);
		$query->execute();
		$result = $query->fetch();
		if($result){
			if(intval($result['COUNT']) == $this->game_num_players){
				$this->change_status(5);
				return True;
			}			
		}
		return False;
	}
}

class Game extends Game_player_data{
	protected $db;
	protected $game_id;
	protected $game_player_id_master = 0;
	protected $game_distance = 0.0;
	protected $game_num_players = 0;
	protected $game_players_id = Array();
	protected $game_exists = False;
	protected $game_status = 1;
	function __construct($db, $game_id = False){
		$this->db = $db; 
		$this->game_id = $game_id;
		if($game_id != False){
			$this->load_data();
		}
	}
	
	function create($player, $num_players, $distance){
		if($this->game_id) return False;
		$player_id = $player->get_id();
		$this->db->insert('game', Array(
				'game_player_id_master' => $player_id,
				'game_distance' => $distance,
				'game_num_players' => $num_players,
				'game_players_id' => json_encode(Array($player_id))
				));
		$this->game_id = $this->db->lastInsertId();
		$this->set_data($distance, $num_players, $player_id, json_encode(Array($player_id)));
		return $this->game_id;		
	}
	
	private function load_data(){
		$query = $this->db->prepare("SELECT * FROM game where game_id = ?");
		$query->bindValue(1, $this->game_id);
		$query->execute();
		$result = $query->fetchAll();
		if(sizeof($result) > 0){
			$this->set_data($result[0]);
			
		}
	}
	
	private function set_data($data){
		$this->game_distance = $data['game_distance'];
		$this->game_num_players = $data['game_num_players'];
		$this->game_player_id_master = intval($data['game_player_id_master']);
		$this->game_status = intval($data['game_status']);
		$this->game_players_id = json_decode($data['game_players_id']);
		$this->game_exists = True;
	}
	
	private function update_players_id($player_id){
		if(count($this->game_players_id) == $this->game_num_players){
			return False;
		}
		if(in_array($this->game_players_id, Array($player_id))){
			return -1;
		}else{
			array_push($this->game_players_id, $player_id);
			$this->db->update('game', Array('game_players_id' => json_encode($this->game_players_id)),
					Array('game_id' => $this->game_id));
			if(count($this->game_players_id) == $this->game_num_players){
				$this->change_status(2);
			}
			return True;
		}
	}
	
	function start(){
		$this->change_status(4);
	}
	
	function player_start($player, $date){
		$this->player_data_create($player);
		$this->player_data_set_start($player, $date);
		$this->player_data_start_all();
	}
	
	
	function player_finish($player, $date){
		$this->player_data_set_end($player, $date);
	}
	
	function exists(){
		return $this->game_exists;
	}
	
	function join_player($player){
		$player_id = $player->get_id();
		return $this->update_players_id($player_id);
	}
	
	function get_id(){
		return $this->game_id;
	}

	
	function get_distance(){
		return $this->game_distance;
	}
	
	function get_players(){
		return $this->game_players_id;
	}
	
	function get_master_id(){
		return $this->game_player_id_master;
	}
	
	function get_status(){
		/* 
		 * 1: wait_players
		 * 2: full
		 * 3: ready
		 * 4: starting
		 * 5: in progress
		 * 6: finish
		 */
		return $this->game_status;
	}
	
	protected function change_status($status){
		$this->status = $status;
		$this->db->update('game', Array('game_status' => $this->status),
				Array('game_id' => $this->game_id));
	}
	
}

?>