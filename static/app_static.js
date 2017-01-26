var app = angular.module("todolist", []);

app.controller("list_controller", function($scope) {
    $scope.items = [

		{
			"id": 1,
			"subject": "Teach at RNSIT"
		},

		{
			"id": 1,
			"subject": "Teach at RVCE"
		},

		{
			"id": 1,
			"subject": "Teach at PESIT"
		}
	];
});