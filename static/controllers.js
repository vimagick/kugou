var kugouControllers = angular.module('kugouControllers', []);

kugouControllers.controller('SongListCtrl', function ($scope, $http) {
    $http.get('/hotsong/hit?max_results=100').success(function(data) {
        $scope.songs = data._items;
    });
});

kugouControllers.controller('SongDetailCtrl', function($scope, $http, $routeParams) {
    var songId = $routeParams.songId;
    $http.get('/resolve/' + songId).success(function(data) {
        $scope.url = data.url;
    });
});
