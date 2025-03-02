// map.js

// This will run after the DOM has loaded
document.addEventListener("DOMContentLoaded", function () {
    // Get markers passed from FastAPI into JavaScript
    var markers = JSON.parse(document.getElementById('markers-data').textContent);
  
    // Initialize the map and set the view (center and zoom level)
    var map = L.map('map').setView([44.5646, -123.2620], 14);  // Centered on University of Oregon with zoom level 14
  
    // Set up the OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
  
    // Loop through the markers array and create markers dynamically
    markers.forEach(function(markerData) {
      var marker = L.marker([markerData.lat, markerData.lng]).addTo(map);
      marker.bindPopup("<b>" + markerData.info + "</b>");
  
      // Event listener for when the marker is clicked
      marker.on('click', function() {
        // Update the info section with new content
        document.getElementById('info-section').innerHTML = `
          <h3>Marker Information</h3>
          <p>${markerData.info}</p>
          <p>Latitude: ${markerData.lat}</p>
          <p>Longitude: ${markerData.lng}</p>
        `;
      });
    });
  });
  