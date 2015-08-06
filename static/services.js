var kugouServices = angular.module('kugouServices', ['ngResource']);

kugouServices.factory('KuGou', function($resource){
    return $resource('', {}, {
        resolve: {url:'resolve/:songHash', method:'GET'},
        hotsong: {url:'hotsong/:songType?max_results=15', method:'GET'},
        newsong: {url:'newsong/:songType?max_results=15', method:'GET'},
    });
});
