document.addEventListener("DOMContentLoaded", function () {
  getLocation();
  //   initMap();
});

// Get user's location
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(validateLocation);
  } else {
    console.log("Geolocation is not supported by this browser.");
  }
}

// Send user's location to server
function validateLocation(position) {
  const loc = {
    latitude: position.coords.latitude,
    longitude: position.coords.longitude,
  };
  fetch("/perkuliahan/jadwal/linimasa/tandai-presensi/get-user-location", {
    method: "POST",
    headers: {
      "Content-Type": "application/json", // Set Content-Type to application/json
    },
    body: JSON.stringify({ location: loc }),
  })
    .then((response) => {
      //   console.log("response: ", response);
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Server error: " + response.statusText);
      }
    })
    .then((data) => {
      if (data.status === "success") {
        // render map
        const map = document.getElementById("map");
        map.innerHTML = data.data["mapElements"];

        // distance logic
        const distance = data.data["distance"];
        if (distance > 50) {
          // $('.toast').toast('show');
          console.log("You are too far from the location");
        }
        console.log("Distance: ", distance);
      } else {
        console.log("Location is invalid");
      }
    })
    .catch((error) => {
      console.log("Request failed: ", error);
    });
}
