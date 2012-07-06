var map;

var boundsLookup = {};

$(document).ready(function() {

    map = new L.Map('map');

    var tileUrl = 'http://{s}.tiles.mapbox.com/v3/mapbox.mapbox-light/{z}/{x}/{y}.png',
        tileAttrib = 'Map tiles from MapBox (<a href="http://mapbox.com/about/maps/">terms</a>) and OpenStreetMap ',
        tileLayer = new L.TileLayer(tileUrl, {maxZoom: 24, attribution: tileAttrib});
        
    map.setView(new L.LatLng(40,-95), 4).addLayer(tileLayer);

    $.getJSON('/gtfs/all.json', function(data) {
    
        var listElements = [];
        
        for(i=0; i<data.length; i++) {

            var daysToExp = data[i].info.days_to_expiration;
            var color = "green";
            if(daysToExp < 0) color = "red";
            else if(daysToExp < 60) color = "yellow";

            var geojson = new L.GeoJSON(data[i].geom);
            geojson.setStyle({ color : color });
            map.addLayer(geojson);

            popupContent = "<b>"+data[i].info.name+"</b><br>";
            popupContent += "Area: "+data[i].info.area+"<br>";
            var date = new Date(parseInt(data[i].info.date_added)*1000);
            popupContent += "Date Added: "+date.toLocaleString()+"<br>";
            date = new Date(parseInt(data[i].info.date_last_updated)*1000);
            popupContent += "Last Updated: "+date.toLocaleString()+"<br>";
            popupContent += "Days to expiration: "+daysToExp+"<br>";
            popupContent += "<a href='"+data[i].info.dataexchange_url+"' target='_blank'>Link to Data Exchange Entry</a>";
            geojson.bindPopup(popupContent);

            var linkid = "link"+i;
            boundsLookup[linkid] = geojson.getBounds();
            
            
            linkHTML = "<div><div class='feedstatus' style='background:"+color+"'></div><div class='feedlink' id='"+linkid+"'>"+data[i].info.name+"</div><div style='clear:both;'></div></div>";

            listElements.push([data[i].info.name, linkHTML, linkid]);
                        
        }
        listElements.sort(function(a, b) {
            a = a[0];
            b = b[0];

            return a < b ? -1 : (a > b ? 1 : 0);
        });
        
        for(var i=0; i<listElements.length; i++) {
            $('#list').append(listElements[i][1]);
            $("#"+listElements[i][2]).click(function() {
                map.fitBounds(boundsLookup[this.id]);
            });                  

        }
    });        
});
