
// Store our API endpoint inside queryUrl
var link = "Resources/World_Data/international_wage_gap_data.csv";

// function for the markerSize depending on magnitude
function markerSize(WageGap) {
  return WageGap;
}

// function to determine the color of markers
function markerColor(WageGap) {
  if (WageGap > 40) {
    return "#E23A28"
  }
  else if (WageGap > 30) {
    return "#AB3E5B"
  }
  else if (WageGap > 20) {
    return "#EF746F"
  }
  else if (WageGap > 10) {
    return "#FFBE40"
  }
  else if (WageGap > 0) {
    return "#ECF081"
  }
  else {
    return "#B3CC57"
  }
}


// Perform a GET request to the query URL
d3.csv(link).then(function (data) {
  console.log(data)
  // Create a GeoJSON layer containing the features array on the earthquakeData object
  // Run the onEachFeature function once for each piece of data in the array
  var earthquakes = L.geoJSON(data.features, {
    onEachFeature: addPopup,
    pointToLayer: addMarker
  });
  createMap(earthquakes);
});

// function addMarker(feature, location) {
//   var options = {
//     stroke: false,
//     color: markerColor(feature.properties.mag),
//     fillColor: markerColor(feature.properties.mag),
//     radius: markerSize(feature.properties.mag)
//   }

//   return L.circleMarker(location, options);
// }


// function addPopup(feature, layer) {
//   return layer.bindPopup("<h3>" + feature.properties.place +
//     "</h3><hr><p>" + new Date(feature.properties.time) + "</p><hr><p>" + feature.properties.mag + "</p>");
// }

// Sending our earthquakes layer to the createMap function
// function createMap(earthquakes) {

//   // Define streetmap and darkmap layers
//   var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
//     attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
//     tileSize: 512,
//     maxZoom: 18,
//     zoomOffset: -1,
//     id: "mapbox/light-v10",
//     accessToken: API_KEY
//   });

//   var darkmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
//     attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
//     maxZoom: 18,
//     id: "dark-v10",
//     accessToken: API_KEY
//   });

//   // Define a baseMaps object to hold our base layers
//   var baseMaps = {
//     "Grayscale Map": lightmap,
//     "Dark Map": darkmap
//   };

//   // Create overlay object to hold our overlay layer
//   var overlayMaps = {
//     Earthquakes: earthquakes
//   };

//   // Create our map, giving it the streetmap and earthquakes layers to display on load
//   var myMap = L.map("map", {
//     center: [
//       37.09, -95.71
//     ],
//     zoom: 3,
//     layers: [lightmap, earthquakes]
//   });

//  // Create a legend for the map based on the earthquakes data and colors
//  var legend = L.control({position: "bottomright"});
//  legend.onAdd = function() {
//      var div = L.DomUtil.create("div", "info legend");
//      var colors =["#E23A28","#AB3E5B","#EF746F","#FFBE40","#ECF081","#B3CC57"];
//      var legendLabel = "<h3>Earthquake intensity</h3>" + 
//          "<div class='labels'>" +
//              "<div class='max'>5+</div>" +
//              "<div class=\"four\">4-5</div>" +
//              "<div class=\"three\">3-4</div>" +
//              "<div class=\"two\">2-3</div>" +
//              "<div class=\"one\">1-2</div>" +
//              "<div class=\"min\">0-1</div>" +
//          "</div>";

//      div.innerHTML = legendLabel;
//      var labels = [];
//      colors.forEach(function(color) {
//          labels.push("<li style='background-color:" + color +"'></li>");
//      });

//      div.innerHTML += "<ul id = 'legendcolors'>" + labels.join("") + "</ul>";
//      return div;
//  };
//  // Append label to the map
//  legend.addTo(myMap);

//   // Create a layer control
//   // Pass in our baseMaps and overlayMaps
//   // Add the layer control to the map
//   L.control.layers(baseMaps, overlayMaps, {
//     collapsed: true
//   }).addTo(myMap);
// }
