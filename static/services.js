var kugouServices = angular.module('kugouServices', ['ngResource']);

kugouServices.factory('KuGou', function($resource){
    return $resource('', {}, {
        resolve: {url:'resolve/:songHash', method:'GET'},
        hotsong: {url:'hotsong/:songType', method:'GET'},
        newsong: {url:'newsong/:songType', method:'GET'},
    });
});
