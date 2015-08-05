var kugouApp = angular.module('kugouApp', ['ngRoute', 'kugouControllers']);

kugouApp.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
}).config(function($routeProvider) {
    $routeProvider.when('/songs', {
        templateUrl: '/static/song-list.html',
        controller: 'SongListCtrl'
    }).when('/songs/:songId', {
        templateUrl: '/static/song-detail.html',
        controller: 'SongDetailCtrl'
    }).otherwise({
        redirectTo: '/songs'
    });
});

