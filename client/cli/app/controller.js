app = angular.module("pt_cycling", ["ngRoute", "ngStorage"]);
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
	["$scope", "$localStorage", "$location", "$interval", 
	function($scope, $localStorage, $location, $interval){
	$scope.$storage = $localStorage.$default({
		'settings': {
			user_name: '',
			ip_server:  '',
			bike_shot: {id: 26, name: 26}
		}
    });
	$scope.settings = $scope.$storage.settings;
	$scope.form = {};
	$scope.form.bike_shot_options = [
		{
			id: 26, name: 26
		},
		{
			id: 27.5, name: 27.5
		},
		{
			id: 28, name: 28
		},
		{
			id: 29, name: 29
		}
	];

	$scope.settings_copy = {};
	angular.copy($scope.settings, $scope.settings_copy);
	
	$scope.create_game = {}
	$scope.create_game.distance = 1;
	$scope.create_game.number_of_players = 1;
	
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
	
	$scope.save_settings = function(){
		$scope.$storage.settings = $scope.settings_copy;
		$scope.settings = $localStorage;
		$scope.go_home();
	};

	$scope.create_game = function (){
		$scope.go_game();
	};

	$scope.join_game = function(){
		$scope.go_game();
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
}]);
	