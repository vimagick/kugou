var kugouControllers = angular.module('kugouControllers', []);

kugouControllers.controller('SongListCtrl', function ($scope, $routeParams, KuGou) {
    $scope.songs = KuGou.hotsong({songType: $routeParams.songType}, function(data) {
        $scope.songs = data._items;
    });
});

kugouControllers.controller('SongDetailCtrl', function($scope, $routeParams, KuGou) {
    $scope.song = KuGou.resolve({songHash: $routeParams.songHash}, function(data) {
        $scope.song = data;
    });
});
