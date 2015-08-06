var kugouApp = angular.module('kugouApp', ['ngRoute', 'kugouControllers', 'kugouServices']);

kugouApp.config(function($routeProvider) {
    $routeProvider.when('/hotsong/:songType', {
        templateUrl: 'static/song-list.html',
        controller: 'SongListCtrl'
    }).when('/songs/:songHash', {
        templateUrl: 'static/song-detail.html',
        controller: 'SongDetailCtrl'
    }).when('/search/:keyword', {
        templateUrl: 'static/song-search.html',
        controller: 'SongSearchCtrl'
    }).otherwise({
        redirectTo: '/hotsong/hit'
    });
});

