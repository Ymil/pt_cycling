
app.controller('game', 
	['$scope', "$interval", "$http" ,
	function ($scope, $interval, $http) {
		//$scope.game = gameServices;
		$scope.flags.start_game = false;
		$scope.flags.end_game = false;
		/*$scope.game.game_id = 0;
		$scope.game.game_distance = 25;
		$scope.game.game_players = {
			1: {
				'name': 'player1',
				'speed': 0,
				'speed_max': 0,
				'distance': 0
			},
			2: {
				'name': 'player2',
				'speed': 0,
				'speed_max': 0,
				'distance': 0
			},
			3: {
				'name': 'player3',
				'speed': 0,
				'speed_max': 0,
				'distance': 0

			}
		};*/
		$scope.start_game = function(){
			$http.get('/start_game');
					
		}

		$scope.start_game_player = function(){			
			$http.get("/start_game_player");
			console.log("Start Game")
		};
		
		$scope.game.get_status = function(){
			$http.get('/status_game').then(function successCallback(response){
				$scope.game.upgradeable = response.data;
				if($scope.game.upgradeable.game_status == 4 && !$scope.flags.start_game){
					$scope.flags.start_game = true;
					$scope.downcount.start(5, $scope.start_game_player);					
					//$interval.cancel($scope.game.i_get_status);
				}else if($scope.game.upgradeable.game_status == 6 && $scope.flags.end_game){
					$interval.cancel($scope.game.i_get_status);
				}
			});
		};

		$scope.$watch("game.upgradeable.game_players", function(newVal,oldVal){
			$scope.game.game_players = Object.keys($scope.game.upgradeable.game_players)
				.map(function(key) {
					return $scope.game.upgradeable.game_players[key];
				});
			if($scope.game.upgradeable.game_status == 5 && !$scope.flags.end_game){
				if(newVal['0']['player_distance'] >= $scope.game.game_distance){
					$http.get("/end_game_player");
					console.log("Finish game");
					$scope.flags.end_game = true;
				}
			}
		});	
		
		$scope.game.i_get_status = $interval($scope.game.get_status, 1000);
		$scope.simulation = function(){
			for( var player_id in $scope.game.game_players){
				var distance = $scope.game.game_players[player_id]['player_distance'];
				$scope.game.game_players[player_id]['player_distance'] = distance + Math.random() * 10 / 10;
				$scope.game.game_players[player_id]['player_speed'] = Math.random() * 10;
				console.log($scope.game.game_players[player_id]['player_distance']);
				if($scope.game.game_players[player_id]['player_distance'] > $scope.game.game_distance ){
					$interval.cancel($scope.sim);
				}
			}
		};
		$scope.$on("$destroy", function handler() {
			$interval.cancel($scope.game.i_get_status);
		});
	}
]);