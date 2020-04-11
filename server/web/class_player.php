<?php 
class Player_data{
	function get_data($game_id){
		$query = $this->db->prepare("SELECT * FROM player_data
				WHERE player_data_game_id = ? AND player_data_player_id = ? 
				ORDER BY player_data_id DESC LIMIT 1");
		$query->bindValue(1, $game_id);
		$query->bindValue(2, $this->player_id);
		$query->execute();
		$result = $query->fetch();
		return $result;
	}
	
	function add_data($game_id, $date, $distance, $speed, $speed_prom,$speed_max){
		/*
		 * $array_data = Array('player_data_date' => '', 'player_data_distance' => 0.0, 'player_data_speed_max' => 0.0);
		 */
		$array_data = Array(
				'player_data_date_player' => $date, 
				'player_data_distance' => floatval($distance),
				'player_data_speed' => floatval($speed),
				'player_data_speed_max' => floatval($speed_max),
				'player_data_speed_prom' => floatval($speed_prom)
		);
		$array_data['player_data_game_id'] = $game_id;
		$array_data['player_data_player_id'] = $this->player_id;
		$this->db->insert('player_data', $array_data);
	}
}

class Player extends Player_data{
	protected $player_id = False;
	protected $player_name = '';
	protected $db;
	function __construct($db, $player_name = False, $player_id = False){
		$this->db = $db;
		$this->player_id = $player_id;
		$this->player_name = $player_name;
		$this->load_data();
	}
	
	private function load_data(){
		if($this->player_id){
			$query = $this->db->prepare("SELECT player_id, player_name from player where player_id = ?");
			$query->bindValue(1, $this->player_id);
		}
		else{
			$query = $this->db->prepare("SELECT player_id, player_name from player where player_name = ?");
			$query->bindValue(1, $this->player_name);
		}
		$query->execute();
		$result = $query->fetch();
		if($result){
			$this->player_id = $result['player_id'];
			$this->player_name = $result['player_name'];
		}else{			
			$this->db->insert('player', Array('player_name' => $this->player_name));
			$this->player_id = $this->db->lastInsertId();
		}
	}
	
	function get_id(){
		return $this->player_id;
	}
	
	function get_name(){
		return $this->player_name;
	}
}
?>