<?php 

class Game{
	protected $db;
	protected $game_id;
	protected $game_player_id_master = 0;
	protected $game_distance = 0.0;
	protected $game_num_players = 0;
	protected $game_players_id = Array();
	protected $game_exists = False;
	
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
				'game_players_id' => json_encode(Array($player_id)),
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
			$this->set_data($result[0]['game_distance'], $result[0]['game_num_players'], 
					$result[0]['game_player_id_master'], $result[0]['game_players_id']);
			
		}
	}
	
	private function set_data($game_distance, $game_num_players, $game_player_id_master, $game_players_id){
		$this->game_distance = $game_distance;
		$this->game_num_players = $game_num_players;
		$this->game_player_id_master = $game_player_id_master;
		
		$this->game_players_id = json_decode($game_players_id);
		$this->game_exists = True;
	}
	
	private function update_players_id($player_id){
		if(sizeof($this->game_players_id) == $this->game_num_players){
			return False;
		}
		if(in_array($this->game_players_id, Array($player_id))){
			return False;
		}else{
			array_push($this->game_players_id, Array($player_id));
			$this->db->update('game', Array('game_players_id' => json_encode($this->game_players_id)),
					Array('game_id' => $this->game_id));
			return True;
		}
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
	
	
}

?>