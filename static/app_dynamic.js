var app = angular.module("todolist", []);

app.controller("list_controller", function($scope) {
    $scope.items = [

	];

	$scope.getAllItems = function(){
		$http({
				method: "GET",
				url: "../item",
				data: {"id": "-1"}	
			}).then(
			function mySucces(response) {
        		$scope.items = response.data;
    		}, function myError(response) {

    		});
		}

	$scope.addItem = function(subject){
		$http({
				method: "PUT",
				url: "../item",
				data: {"item": subject}	
			}).then(
			function mySucces(response) {
        		$scope.items.push(response.data);
    		}, function myError(response) {
    			
    		});
		}
	}

	$scope.delete = function(id){
		$http({
				method: "DELETE",
				url: "../item",
				data: {"id": id}	
			}).then(
			function mySucces(response) {
        		$scope.items = $scope.items.filter(function(o){
        			return o.id != id;
        		});
    		}, function myError(response) {
    			
    		});
		}

	$scope.deleteAll = function(){
		$http({
				method: "DELETE",
				url: "../item",
				data: {"id": "-1"}	
			}).then(
			function mySucces(response) {
        		$scope.items = [];
    		}, function myError(response) {
    			
    		});
		}
	}
});