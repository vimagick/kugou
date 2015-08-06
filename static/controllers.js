var kugouControllers = angular.module('kugouControllers', []);

kugouControllers.controller('MainCtrl', function($scope) {
    $scope.search = function() {
        $('#btn').click();
    }
});

kugouControllers.controller('SongListCtrl', function ($scope, $routeParams, KuGou) {
    $scope.songs = KuGou.hotsong({songType: $routeParams.songType}, function(data) {
        $scope.songs = data._items;
    });
    $scope.songType = $routeParams.songType;
});

kugouControllers.controller('SongSearchCtrl', function ($scope, $routeParams, KuGou) {
    $scope.songs = KuGou.search({keyword: $routeParams.keyword}, function(data) {
        $scope.songs = data._items;
    });
});

kugouControllers.controller('SongDetailCtrl', function($scope, $routeParams, KuGou) {
    $scope.song = KuGou.resolve({songHash: $routeParams.songHash}, function(data) {
        $scope.song = data;
    });
});
