function gameServices(){
	service = {
		id: 0,
		distance: 0,
		players: {}
	};
	return service;
}
app = angular.module("pt_cycling", ["ngRoute", "ngStorage"]);

app.filter('orderObjectBy', function() {
  return function(items, field, reverse) {
    var filtered = [];
    angular.forEach(items, function(item) {
      filtered.push(item);
    });
    filtered.sort(function (a, b) {
      return (a[field] > b[field] ? 1 : -1);
    });
    if(reverse) filtered.reverse();
    return filtered;
  };
});

app.config(function ($routeProvider, $localStorageProvider){
	$routeProvider
		.when("/home",{
			templateUrl: 'views/home.html'
		})
		.when("/settings",{
			templateUrl: 'views/settings.html'
		})
		.when("/create_game", {
			templateUrl: 'views/create_game.html'
		})
		.when("/join_game", {
			templateUrl: 'views/join_game.html'
		})
		.when("/game", {
			templateUrl: 'views/game.html'
		})
		.otherwise({
			redirectTo: '/home'
		});
	$localStorageProvider.get
});
app.controller("controller", 
	["$scope", "$localStorage", "$location", "$interval", "$http",
	function($scope, $localStorage, $location, $interval, $http){
	$scope.flags = {};
	$scope.game = {};
	$scope.game.game_id = 0;
	$scope.game.game_distance = 0;
	$scope.game.game_players = {};
	$scope.game.upgradeable = {};
	$scope.game.upgradeable.game_players = {}
	$scope.game.upgradeable.game_status = 0;
	
	$scope.data_create_game = {}
	$scope.data_create_game.game_distance = 1;
	$scope.data_create_game.number_of_players = 1;
	
	$scope.loading = {};
	$scope.loading.active = false;

	$scope.downcount = {
		'value': 3,
		'active': false,
		'end_signal': '',
		'start': function(n, end_signal){
			$scope.downcount.value = n;
			$scope.downcount.active = true;
			$scope.downcount.end_signal = end_signal;
			$interval($scope.downcount.update, 1000, n);
			console.log('Downcount start');
		},
		'update': function (){			
			$scope.downcount.value = $scope.downcount.value - 1;
			console.log('Downcount update');
			if($scope.downcount.value == 0){
				$scope.downcount.active = false;
				$scope.downcount.end_signal();
				console.log("Downcount end");
			}
		}
	};
	$scope.game = {};
	$scope.create_game = function (){
		$scope.loading.active = true;
		$http.put("/create_game", $scope.data_create_game).then(function successCallback(response){
			$scope.game = response.data;
			$scope.loading.active = false;
			$scope.join_game();
		});
		
	};

	$scope.join_game = function(){
		$scope.loading.active = true;
		$http.get("/join_game/"+$scope.game.game_id).then(function successCallback(response){
			$scope.game.game_distance = response.data.game_distance;
			$scope.game.game_num_players = response.data.game_num_players;
			$scope.loading.active = false;
			$scope.go_game();
		});
		
	}

	$scope.go_home = function(){
		$location.path("/home");
	};
	
	$scope.go_settings = function(){
		$location.path("/settings");
	};

	$scope.go_create_game = function (){
		$location.path("/create_game");
	};

	$scope.go_join_game = function (){
		$location.path("/join_game");
	};

	$scope.go_game = function (){
		$location.path("/game");
	}	
	
	$scope.$storage = $localStorage.$default({
		'settings': {
			user_name: '',
			serial_port: '',
			ip_server:  '',
			bike_shot: 26
		}
    });
	$scope.get_settings = function(){ 
		$http({
		method: 'GET',
		url: '/get_settings'
		}).then(function (response) {
			$scope.$storage.settings = response.data;
			$scope.settings = $scope.$storage.settings;
			if($scope.$storage.settings.user_name == ""){
				$scope.go_settings();
			}
		});
	}
	$scope.get_settings();

}]);
	