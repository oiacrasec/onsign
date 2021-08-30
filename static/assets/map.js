$(document).ready(function () {
    try {
        var obj = captureParams();
        if (validateParams(obj)) {
            $("#map-container").toggleClass('invisible visible');

            var map = new ol.Map({
                target: 'map',
                layers: [
                    new ol.layer.Tile({
                        source: new ol.source.OSM()
                    })
                ],
                view: new ol.View({
                    center: ol.proj.fromLonLat([parseFloat(obj.lng), parseFloat(obj.lat)]),
                    zoom: 12
                })
            });
        }
    } catch (e) {
        console.log(e);
    }
});

function captureParams() {
    if (location.search) {
        var search = location.search.substring(1);
        return JSON.parse(
            '{"' + decodeURI(search).replace(/"/g, '\\"').replace(/&/g, '","').replace(/=/g, '":"') + '"}'
        );
    }
    return {}
}

function validateParams(params) {
    var keys = [];
    _.each(params, function (val, key) {
        if (val) {
            keys.push(key);
        }
    });
    return _.contains(keys, 'lat') && _.contains(keys, 'lng');
}
