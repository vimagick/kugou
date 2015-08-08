var kugouControllers = angular.module('kugouControllers', []);

kugouControllers.controller('MainCtrl', function($scope) {
    $scope.search = function() {
        $('#btn').click();
    }
});

kugouControllers.controller('SongListCtrl', function ($scope, $routeParams, $location, KuGou) {
    $scope.songs = KuGou.hotsong({songType: $routeParams.songType}, function(data) {
        $scope.songs = data._items;
    });
    $scope.songType = $routeParams.songType;
    $scope.songOptions = {
        'hit': {'name': 'HIT', 'rankid': 6666, 'ranktype': 2},
        'top': {'name': 'TOP', 'rankid': 8888, 'ranktype': 2},
        'kugou': {'name': 'KuGou', 'rankid': 4677, 'ranktype': 1},
        'hk': {'name': '香港', 'rankid': 4676, 'ranktype': 1},
        'tw': {'name': '台湾', 'rankid': 4688, 'ranktype': 1},
        'us': {'name': '美国', 'rankid': 4681, 'ranktype': 1},
        'uk': {'name': '英国', 'rankid': 4680, 'ranktype': 1},
        'jp': {'name': '日本', 'rankid': 4673, 'ranktype': 1},
        'kr': {'name': '韩国', 'rankid': 4672, 'ranktype': 1},
        'itunes': {'name': 'iTunes', 'rankid': 4674, 'ranktype': 1},
        'channelv': {'name': 'Channel V', 'rankid': 4694, 'ranktype': 1},
        'ktv': {'name': 'KTV', 'rankid': 4693, 'ranktype': 1},
        'love': {'name': '爱情', 'rankid': 67, 'ranktype': 3},
        'blue': {'name': '忧伤', 'rankid': 65, 'ranktype': 3},
        'heal': {'name': '治愈', 'rankid': 22590, 'ranktype': 3},
    };
    $scope.rankName = function (rankType) {
        return {1: '榜单', 2: '趋势', 3: '分类'}[rankType];
    }
    $scope.listSongs = function (songType) {
        $location.path('/hotsong/' + songType);
    }
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
