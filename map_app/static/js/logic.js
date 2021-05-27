
// Store our API endpoint inside queryUrl
var queryUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson";
var link = "https://raw.githubusercontent.com/miheep8938/female_participation_in_leadership/main/Resources/World_Data/international_wage_gap_data.csv?raw=true";


// function for the markerSize depending on magnitude
function markerSize(magnitude) {
  return magnitude * 5;
}

// function to determine the color of markers
function markerColor(magnitude) {
  if (magnitude > 5) {
    return "#E23A28"
  }
  else if (magnitude > 4) {
    return "#AB3E5B"
  }
  else if (magnitude > 3) {
    return "#EF746F"
  }
  else if (magnitude > 2) {
    return "#FFBE40"
  }
  else if (magnitude > 1) {
    return "#ECF081"
  }
  else {
    return "#B3CC57"
  }
}


// // Perform a GET request to the query URL
// d3.json(queryUrl).then(function (data) {
//   console.log(data)
//   // Create a GeoJSON layer containing the features array on the earthquakeData object
//   // Run the onEachFeature function once for each piece of data in the array
//   var earthquakes = L.geoJSON(data.features, {
//     onEachFeature: addPopup,
//     pointToLayer: addMarker
//   });
//   createMap(earthquakes);
// });

// Perform a GET request to the query URL
d3.csv(link).then(function (data) {
  console.log(data)
  // Create a GeoJSON layer containing the features array on the earthquakeData object
  // Run the onEachFeature function once for each piece of data in the array
  var earthquakes = L.geoJSON(data, {
    onEachFeature: addPopup,
    pointToLayer: addMarker
  });
  createMap(earthquakes);
});

function addMarker(feature, location) {
  // var options = {
  //   stroke: false,
  //   color: markerColor(feature.properties.mag),
  //   fillColor: markerColor(feature.properties.mag),
  //   radius: markerSize(feature.properties.mag)
  // }

  // return L.circleMarker(location, options);
  return L.circleMarker(location);
}


function addPopup(feature, layer) {
  // return layer.bindPopup("<h3>" + feature.properties.place +
  //   "</h3><hr><p>" + new Date(feature.properties.time) + "</p><hr><p>" + feature.properties.mag + "</p>");
  return layer.bindPopup("<h3> Hello World </h3>");
}

// Sending our earthquakes layer to the createMap function
function createMap(earthquakes) {

  // Define streetmap and darkmap layers
  var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
    attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
    tileSize: 512,
    maxZoom: 18,
    zoomOffset: -1,
    id: "mapbox/light-v10",
    accessToken: API_KEY
  });

  var darkmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "dark-v10",
    accessToken: API_KEY
  });

  // Define a baseMaps object to hold our base layers
  var baseMaps = {
    "Grayscale Map": lightmap,
    "Dark Map": darkmap
  };

  // Create overlay object to hold our overlay layer
  var overlayMaps = {
    Earthquakes: earthquakes
  };

  // Create our map, giving it the streetmap and earthquakes layers to display on load
  var myMap = L.map("map", {
    center: [
      37.09, -95.71
    ],
    zoom: 3,
    layers: [lightmap, earthquakes]
  });

  // Create a legend for the map based on the earthquakes data and colors
  var legend = L.control({ position: "bottomright" });
  legend.onAdd = function () {
    var div = L.DomUtil.create("div", "info legend");
    var colors = ["#E23A28", "#AB3E5B", "#EF746F", "#FFBE40", "#ECF081", "#B3CC57"];
    var legendLabel = "<h3>Earthquake intensity</h3>" +
      "<div class='labels'>" +
      "<div class='max'>5+</div>" +
      "<div class=\"four\">4-5</div>" +
      "<div class=\"three\">3-4</div>" +
      "<div class=\"two\">2-3</div>" +
      "<div class=\"one\">1-2</div>" +
      "<div class=\"min\">0-1</div>" +
      "</div>";

    div.innerHTML = legendLabel;
    var labels = [];
    colors.forEach(function (color) {
      labels.push("<li style='background-color:" + color + "'></li>");
    });

    div.innerHTML += "<ul id = 'legendcolors'>" + labels.join("") + "</ul>";
    return div;
  };
  // Append label to the map
  legend.addTo(myMap);

  // Create a layer control
  // Pass in our baseMaps and overlayMaps
  // Add the layer control to the map
  L.control.layers(baseMaps, overlayMaps, {
    collapsed: true
  }).addTo(myMap);
}

// Tried another way and it's also working
// Store our API endpoint inside queryUrl
// var queryUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson";
// // Perform a GET request to the query URL
// d3.json(queryUrl).then(function (data) {
//     createFeatures(data.features);
//     // console.log(data.features)
// });
// function createFeatures(earthquakeData) {
//     // Define a function we want to run once for each feature in the features array
//     // Give each feature a popup describing the place and time of the earthquake
//     function onEachFeature(feature, layer) {
//         layer.bindPopup("<h3>" + feature.properties.place +
//             "</h3><hr><p>" + new Date(feature.properties.time) + "</p>");
//     }
//     function markerSize(magnitude) {
//         return magnitude * 10000;
//     }
//     function markerColor(magnitude) {
//         if (magnitude > 5) {
//           return "#D7301F"
//         }
//         else if (magnitude > 4) {
//           return "#EAA92C"
//         }
//         else if (magnitude > 3) {
//           return "#F7DB11"
//         }
//         else if (magnitude > 2) {
//           return "#92EA2C"
//         }
//         else if (magnitude > 1) {
//           return "#2CEABF"
//         }
//         else {
//           return "#2C99EA"
//         }
//       }
//     // Create a GeoJSON layer containing the features array on the earthquakeData object
//     // Run the onEachFeature function once for each piece of data in the array
//     var earthquakes = L.geoJSON(earthquakeData, {
//         pointToLayer:function(earthquakeData,latlng){
//             return L.circle(latlng, {
//                 radius:markerSize(earthquakeData.properties.mag),
//                 color:markerColor(earthquakeData.properties.mag)
//             });
//         },
//         onEachFeature: onEachFeature
//     });
//     // Sending our earthquakes layer to the createMap function
//     createMap(earthquakes);
// }
// function createMap(earthquakes) {
//     // Define streetmap and darkmap layers
//     var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
//         attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
//         tileSize: 512,
//         maxZoom: 18,
//         zoomOffset: -1,
//         id: "mapbox/light-v10",
//         accessToken: API_KEY
//     });
//     var darkmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
//         attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
//         maxZoom: 18,
//         id: "dark-v10",
//         accessToken: API_KEY
//     });
//     // var earthquakeLayer = L.layerGroup(earthquakeMarker);
//     var newLayer = new L.LayerGroup();
//     // Define a baseMaps object to hold our base layers
//     var baseMaps = {
//         "Light Map": lightmap,
//         "Dark Map": darkmap
//     };
//     // Create overlay object to hold our overlay layer
//     var overlayMaps = {
//         Earthquakes: earthquakes
//     };
//     // Create our map, giving it the lightmap and earthquakes layers to display on load
//     var myMap = L.map("map", {
//         center: [
//             37.09, -95.71
//         ],
//         zoom: 5,
//         layers: [lightmap, earthquakes,newLayer]
//     });
//     // Create a layer control
//     // Pass in our baseMaps and overlayMaps
//     // Add the layer control to the map
//     L.control.layers(baseMaps, overlayMaps, {
//         collapsed: false
//     }).addTo(myMap);
// }