app.controller('game', 
	['$scope', "$interval", 
	function ($scope, $interval) {
		$scope.game = {};
		$scope.game.id = 0;
		$scope.game.distance = 25;
		$scope.game.players = {
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
		};
		$scope.start_game = function(){
			$scope.downcount.start(5, $scope.start_simulation);
		}
		$scope.start_simulation = function(){
			$scope.sim = $interval($scope.simulation, 1000);
		};

		$scope.simulation = function(){
			for( var player_id in $scope.game.players){
				var distance = $scope.game.players[player_id]['distance'];
				$scope.game.players[player_id]['distance'] = distance + Math.random() * 10 / 10;
				$scope.game.players[player_id]['speed'] = Math.random() * 10;
				console.log($scope.game.players[player_id]['distance']);
				if($scope.game.players[player_id]['distance'] > $scope.game.distance ){
					$interval.cancel($scope.sim);
				}
			}
		};
	}
]);