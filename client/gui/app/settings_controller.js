app.controller('settings', 
	['$scope', "$interval", "$localStorage", "$http",  
	function ($scope, $interval, $localStorage, $http) {
		console.log("Settings constructor");
		$scope.loading.active  = true;
		$scope.settings_copy = {};
		angular.copy($scope.settings, $scope.settings_copy);
		$scope.form = {};
		/*$scope.form.bike_shot_options = [
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
		];*/

		$scope.form.bike_shot_options = [ 26, 27.5, 28, 29 ];
		
		$http.get("/get_serial_ports").then(function (response){
			$scope.form.serial_port = response.data;
			$scope.loading.active = false;
		});

		$scope.save_settings = function(){		
			$scope.loading.active = true;	
			$scope.$storage.settings = $scope.settings_copy;
			$scope.settings = $localStorage.settings;
			$http.put("/set_settings", $scope.settings).then(function (){
				$scope.loading.active = false;
				$scope.get_settings();
				$scope.go_home();
			});			
		}
}
]);