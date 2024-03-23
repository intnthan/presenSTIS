const presensiModal = document.getElementById("presensiModal");
const closeModalPresensi = document.getElementById("closeModalPresensi");
let eventSource;
const pertemuanTerkait = document.getElementById("pertemuan-terkait");

// generate pertemuan terkait
function renderPertemuanTerkait() {
  const row = document.createElement("div");
  const col = document.createElement("div");
  col.className = "col-12 p-0";
  const card = document.createElement("div");
  card.className = "card d-flex align-items-around";
  const cardBody = document.createElement("div");
  cardBody.className = "card-body p-0";
  const flexrow = document.createElement("div");
  flexrow.className = "d-flex flex-row pr-4";
  const icon = document.createElement("i");
  icon.className = "ti-clipboard text-info icon-md mr-2";
  const infoMk = document.createElement("div");
  infoMk.className = "col-8";
  const mk = document.createElement("h6");
  mk.className = "font-weight-bold text-left";
  mk.textContent = "Pemrograman Berbasis Web";
  const dosen = document.createElement("p");
  dosen.className = "text-muted mt-2 card-text";
  dosen.textContent = "Nori Wilantika, S.S.T., M.T.I";
  const status = document.createElement("div");
  status.className = "col-4 px-2";
  const badge = document.createElement("div");
  badge.className = "badge badge-info my-2";
  badge.textContent = "Tepat waktu";

  infoMk.appendChild(mk);
  infoMk.appendChild(dosen);
  status.appendChild(badge);
  flexrow.appendChild(icon);
  flexrow.appendChild(infoMk);
  flexrow.appendChild(status);
  cardBody.appendChild(flexrow);
  card.appendChild(cardBody);
  col.appendChild(card);
  row.appendChild(col);
  pertemuanTerkait.appendChild(row);
}

// render timeline element
function renderTimeline(timelineElements, presensi) {
  // cek udah presensi atau belum
  timelineElements.forEach(function (element) {
    // code untuk styling
    let bg_color, icon;
    const id_title = element.id_title;
    const ul = document.getElementById("timeline-with-icons");

    // switch case for icon and bg color
    switch (id_title) {
      // pertemuan belum dimulai
      case "1":
        bg_color = "bg-info";
        icon = "";
        break;
      // presensi dibuka
      case "2":
        bg_color = "bg-info";
        icon = "ti-write text-white";
        break;
      // // presensi belum ditandai
      // case "3":
      //   bg_color = "bg-warning";
      //   icon = "ti-alert text-white";
      //   break;

      // pertemuan dimulai
      case "5":
        bg_color = "bg-success";
        icon = "ti-control-play text-white";
        break;
      // pertemuan sedang berjalan
      case "6":
        bg_color = "bg-info";
        icon = "ti-timer text-white";
        break;
      // pertemuan selesai
      case "7":
        bg_color = "bg-success";
        icon = "ti-check text-white";
        break;
      default:
        bg_color = "bg-info";
        icon = "";
    }

    // code for rendering timeline element
    const li = document.createElement("li"); // create li element
    li.className = "timeline-item mb-2";
    li.id = "timeline-item-" + element.id_title;
    const span = document.createElement("span"); // create span element inside li
    span.className = "timeline-icon " + bg_color;
    const i = document.createElement("i"); // create i element inside span
    i.className = icon;
    span.appendChild(i);
    const h5 = document.createElement("h5"); // create h5 element inside li
    h5.className = "fw-bold";
    h5.textContent = element.title;
    li.appendChild(span);
    li.appendChild(h5);

    if (element.jam != "None") {
      const p_jam = document.createElement("p"); // create p element inside li
      p_jam.className = "text-muted mb-2 fw-bold";
      p_jam.textContent = element.jam;
      li.appendChild(p_jam);
    }

    if (element.id_title == "2") {
      if (!presensi) {
        li.appendChild(renderPresensiSection());
      } else {
        ul.appendChild(renderMarkedPresensiSection(presensi[0].waktu));
      }
    }

    ul.appendChild(li);
  });
}

// render marked presensi section
function renderMarkedPresensiSection(waktu) {
  bg_color = "bg-success";
  icon = "ti-check text-white";

  // code for rendering timeline element
  const li = document.createElement("li"); // create li element
  li.className = "timeline-item mb-2";
  li.id = "timeline-item-marked";
  const span = document.createElement("span"); // create span element inside li
  span.className = "timeline-icon " + bg_color;
  const i = document.createElement("i"); // create i element inside span
  i.className = icon;
  span.appendChild(i);
  const h5 = document.createElement("h5"); // create h5 element inside li
  h5.className = "fw-bold";
  h5.textContent = "Presensi Ditandai";
  li.appendChild(span);
  li.appendChild(h5);

  const p_jam = document.createElement("p"); // create p element inside li
  p_jam.className = "text-muted mb-2 fw-bold";
  p_jam.textContent = "Waktu presensi : " + waktu;
  li.appendChild(p_jam);

  return li;
}

// render prensensi section when id_title == 2
function renderPresensiSection() {
  const presensiSection = document.createElement("div");
  presensiSection.id = "presensi-section";

  // keterangan presensi
  const presensiTextContainer = document.createElement("div");
  presensiTextContainer.className = "row";
  const presensiTextCol = document.createElement("div");
  presensiTextCol.className = "col grid-margin-md-0 stretch-card";
  const presensiText = document.createElement("p");
  presensiText.textContent = "Presensi telah dibuka, klik tombol dibawah ini untuk melakukan presensi";
  presensiTextCol.appendChild(presensiText);
  presensiTextContainer.appendChild(presensiTextCol);

  // map untuk lihat lokasi
  const mapContainer = document.createElement("div");
  mapContainer.className = "row";
  const mapContainerCol = document.createElement("div");
  mapContainerCol.className = "col grid-margin grid-margin-md-0 stretch-card";
  const card = document.createElement("div");
  card.className = "card";
  const cardBody = document.createElement("div");
  cardBody.className = "card-body p-0";
  const map = document.createElement("div");
  map.id = "map";
  cardBody.appendChild(map);
  card.appendChild(cardBody);
  mapContainerCol.appendChild(card);
  mapContainer.appendChild(mapContainerCol);

  // button presensi
  const presensiButtonContainer = document.createElement("div");
  presensiButtonContainer.className = "row";
  const presensiButtonCol = document.createElement("div");
  presensiButtonCol.className = "col grid-margin grid-margin-md-0 stretch-card mt-2";
  const presensiButton = document.createElement("a");
  presensiButton.id = "presensi-button";
  presensiButton.className = "btn btn-primary";

  // get location
  getLocation()
    .then((distance) => {
      if (distance <= 50) {
        presensiButton.setAttribute("href", "#");
        presensiButton.setAttribute("onclick", "pindai_wajah()");
      } else {
        presensiButton.setAttribute("href", "#");
        presensiButton.setAttribute("onclick", "showLocationAlert()");
      }
    })
    .catch((error) => {
      console.error("Error: ", error);
    });

  presensiButton.textContent = "Tandai kehadiran";
  presensiButtonCol.appendChild(presensiButton);
  presensiButtonContainer.appendChild(presensiButtonCol);

  presensiSection.appendChild(presensiTextContainer);
  presensiSection.appendChild(mapContainer);
  presensiSection.appendChild(presensiButtonContainer);
  return presensiSection;
}

// Get user's location and distance from kampus
function getLocation() {
  return new Promise((resolve, reject) => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          validateLocation(position)
            .then((distance) => {
              resolve(distance);
            })
            .catch((error) => {
              reject(error);
            });
        },
        (error) => {
          reject(error);
        }
      );
    } else {
      reject("Geolocation is not supported by this browser.");
    }
  });
}

// Send user's location to server
function validateLocation(position) {
  return new Promise((resolve, reject) => {
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

          // distance
          const distance = data.data["distance"];
          resolve(distance);
        } else {
          reject("Error: ", data.message);
        }
      })
      .catch((error) => {
        reject("Request failed: ", error);
      });
  });
}

// show alert
function showLocationAlert() {
  Swal.fire({
    title: "Presensi Gagal!",
    text: "Anda harus berada dalam jarak 50 meter untuk melakukan presensi.",
    icon: "warning",
    showConfirmButton: true,
    confirmButtonColor: "#3085d6",
    allowOutsideClick: false,
    // confirmButtonText: '<a href="#" class="text-white close-alert">OK</a>',
    confirmButtonText: "OK",
  });
}

function pindai_wajah() {
  const src = "/perkuliahan/jadwal/linimasa/tandai-presensi/pindai-wajah/marked";
  Swal.fire({
    html: '<img src="/perkuliahan/jadwal/linimasa/tandai-presensi/pindai-wajah" alt="Camera untuk memindai wajah" width="100%" id="camera-container" />',
    showCancelButton: true,
    showConfirmButton: true,
    allowOutsideClick: false,
    confirmButtonText: '<a onclick="mark_attendance()" class="text-white">Tandai presensi</a>',
    cancelButtonColor: "#d33",
    cancelButtonText: '<a href="/perkuliahan/jadwal/linimasa/tandai-presensi/pindai-wajah/stop" class="text-white">Batal</a>',
  });
}

function getnim() {
  fetch("/perkuliahan/get-nim", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      sessionStorage.setItem("nim", data.nim);
      return data.nim;
    });
}

function mark_attendance() {
  fetch("/perkuliahan/jadwal/linimasa/tandai-presensi/pindai-wajah/marked", {
    method: "POST",
    headers: {
      "Content-Type": "application/json", // Set Content-Type to application/json
    },
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Server error: " + response.statusText);
      }
    })
    .then((data) => {
      if (data.status === "success") {
        if (data.attendance === "marked") {
          Swal.fire({
            title: "Presensi Berhasil ditandai!",
            icon: "success",
            showConfirmButton: false,
            timer: 3000,
          });
          location.reload();
        } else {
          Swal.fire({
            title: "Presensi Gagal!",
            text: data.message,
            icon: "error",
            confirmButtonColor: "#3085d6",
            confirmButtonText: '<a href="#" class="text-white close-alert">OK</a>',
          }).then(() => {
            Swal.close();
            pindai_wajah();
          });
        }
      } else {
        throw new Error("Error: " + data.message);
      }
    })
    .catch((error) => {
      console.error("Error: ", error);
    });
}

function closeAlert() {
  fetch("/perkuliahan/jadwal/linimasa/tandai-presensi/pindai-wajah/stop", {
    method: "POST",
    headers: {
      "Content-Type": "application/json", // Set Content-Type to application/json
    },
  }).then((response) => {
    if (response.ok) {
      Swal.close();
      location.reload();
    } else {
      console.log("failed to stop");
      throw new Error("Server error: " + response.statusText);
    }
  });
}
