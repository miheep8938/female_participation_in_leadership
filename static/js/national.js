
// Store our API endpoint inside queryUrl
var queryUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson";
var link = "https://raw.githubusercontent.com/miheep8938/female_participation_in_leadership/main/Resources/international_wage_gap.json?raw=true";
// function for the markerSize depending on magnitude
function markerSize(WageGap) {
  return WageGap * 2;
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
d3.json(link).then(function (data) {
  console.log(data)
  var year = 2018
  filtered_data = data.features.filter(country => country.properties.Time === year)
  console.log(filtered_data)
  // Create a GeoJSON layer containing the features array on the earthquakeData object
  // Run the onEachFeature function once for each piece of data in the array
  // var earthquakes = L.geoJSON(data.features, {
  var genderWageGap = L.geoJSON(filtered_data, {
    onEachFeature: addPopup,
    pointToLayer: addMarker
  });
  createMap(genderWageGap);
});
function addMarker(feature, location) {
  var options = {
    // stroke: false,
    color: markerColor(feature.properties.WageGap),
    fillColor: markerColor(feature.properties.WageGap),
    radius: markerSize(feature.properties.WageGap),
    fillOpacity: 0.75,
  }
  return L.circleMarker(location, options);
  // return L.circleMarker(location);
}
function addPopup(feature, layer) {
  // return layer.bindPopup("<h3>" + feature.properties.place +
  //   "</h3><hr><p>" + new Date(feature.properties.time) + "</p><hr><p>" + feature.properties.mag + "</p>");
  return layer.bindPopup("<h3>" + feature.properties.Country + "</h3><hr><p> Year: " + feature.properties.Time + "</p><hr><p>Wage Gap: " + feature.properties.WageGap + "</p");
}
// Sending our earthquakes layer to the createMap function
function createMap(genderWageGap) {
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
    genderWageGap: genderWageGap
  };
  // Create our map, giving it the streetmap and earthquakes layers to display on load
  var myMap = L.map("map", {
    center: [
      37.09, -95.71
    ],
    zoom: 3,
    layers: [lightmap, genderWageGap]
  });
  // Create a legend for the map based on the earthquakes data and colors
  var legend = L.control({ position: "bottomright" });
  legend.onAdd = function () {
    var div = L.DomUtil.create("div", "info legend");
    var colors = ["#E23A28", "#AB3E5B", "#EF746F", "#FFBE40", "#ECF081", "#B3CC57"];
    var legendLabel = "<h3>Wage Gap Indicator</h3>" +
      "<div class='labels'>" +
      "<div class='max'>40+</div>" +
      "<div class=\"four\">30-40</div>" +
      "<div class=\"three\">20-30</div>" +
      "<div class=\"two\">10-20</div>" +
      "<div class=\"one\">0-10</div>" +
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
  // var newLayer = new L.LayerGroup(); 
  // d3.json(link).then(function (data) {
  //   console.log(data)
  //   var year2010 = 2010
  //   data2010 = data.features.filter(country => country.properties.Time === year2010)
  //   console.log(data2010)
  //   // Create a GeoJSON layer containing the features array on the earthquakeData object
  //   // Run the onEachFeature function once for each piece of data in the array
  //   // var earthquakes = L.geoJSON(data.features, {
  //   var newLayer = L.geoJSON(data2010, {
  //     onEachFeature: addPopup,
  //     pointToLayer: addMarker
  //   }).addTo(newLayer);
  // });
}