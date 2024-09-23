let map;
let service;
let infowindow;

function initMap() {
    const userLocation = { lat: 33.7490, lng: -84.3880 }; // Atlanta location

    map = new google.maps.Map(document.getElementById('map'), {
        center: userLocation,
        zoom: 13
    });

    service = new google.maps.places.PlacesService(map);

    // Handle search button click
    document.getElementById('search-button').addEventListener('click', function() {
        const query = document.getElementById('search-bar').value;
        const minRating = parseFloat(document.getElementById('min-rating').value) || 0; // Default to 0
        const maxDistance = parseFloat(document.getElementById('max-distance').value) || Infinity; // Default to Infinity
        searchPlaces(query, minRating, maxDistance);
    });
}

function searchPlaces(query, minRating, maxDistance) {
    console.log('Searching for:', query);

    const request = {
        query: query,
        fields: ['name', 'geometry', 'rating'], // Include 'rating'
        locationBias: { lat: 33.7490, lng: -84.3880 } // Location bias towards Atlanta
    };

    service.findPlaceFromQuery(request, function(results, status) {
        console.log('Status:', status);

        if (status === google.maps.places.PlacesServiceStatus.OK && results.length) {
            // Filter results by rating and distance
            const userLocation = new google.maps.LatLng(33.7490, -84.3880);
            const filteredResults = results.filter(place => {
                return place.rating >= minRating; // Filter by minimum rating
            }).filter(place => {
                const placeLocation = place.geometry.location;
                const distance = google.maps.geometry.spherical.computeDistanceBetween(userLocation, placeLocation);
                return distance <= maxDistance; // Filter by maximum distance
            });

            if (filteredResults.length > 0) {
                const place = filteredResults[0]; // Take the first filtered result
                if (place.geometry && place.geometry.location) {
                    map.setCenter(place.geometry.location);
                    map.setZoom(15);
                    clearMarkers();

                    const marker = new google.maps.Marker({
                        position: place.geometry.location,
                        map: map,
                        title: place.name
                    });

                    infowindow = new google.maps.InfoWindow({
                        content: place.name
                    });
                    marker.addListener('click', function() {
                        infowindow.open(map, marker);
                    });
                }
            } else {
                alert('No results found matching your filters.');
            }
        } else {
            alert('Place not found or no results returned.');
        }
    });
}

// Optional: Function to clear existing markers if you want to reset the map
function clearMarkers() {
    // Implement logic to clear any existing markers if needed
}

// Load Google Maps API with Places Library
function loadGoogleMapsAPI() {
    const script = document.createElement('script');
    script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyBRWVo1v50HrzJZ_ckYSR7WbR3vWwroh0Q&libraries=places&callback=initMap";
    script.async = true;
    document.head.appendChild(script);
}

window.onload = loadGoogleMapsAPI;
