
app.controller('game', 
	['$scope', "$interval", "$http" ,
	function ($scope, $interval, $http) {
		//$scope.game = gameServices;
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
			$http.get('/start_game/'+$scope.game.id);
			
		}
		$scope.start_simulation = function(){			
			$scope.sim = $interval($scope.simulation, 1000);
		};
		
		$scope.game.get_status = function(){
			$http.get('/status_game/'+$scope.game.id).then(function successCallback(response){
				$scope.game.status = response.data.status;
				if($scope.game.status == 4){
					$scope.downcount.start(5, $scope.start_simulation);
					$interval.cancel($scope.game.i_get_status);
				}
				$scope.game.players = response.data.players;
			});
		};

		$scope.game.i_get_status = $interval($scope.game.get_status, 1000);
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