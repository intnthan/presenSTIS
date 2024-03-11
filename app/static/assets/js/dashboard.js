// set current date and time
function setCurrentDateTime() {
  const currDateElement = document.getElementById("currentDate");
  const currTimeElement = document.getElementById("currentTime");

  const now = new Date();
  const options = { weekday: "long", year: "numeric", month: "long", day: "numeric" };
  const date = now.toLocaleDateString("id-ID", options);
  let time = now.toLocaleTimeString("id-ID");
  time = time.replace(/\./g, ":");
  currDateElement.innerHTML = date;
  currTimeElement.innerHTML = time + "  WIB";
}

// panggil setCurrentDateTime setiap 1 detik
setInterval(setCurrentDateTime, 1000);

// panggil setCurrentDateTime saat halaman pertama kali di-load
setCurrentDateTime();
// panggil setPerkuliahan saat halaman pertama kali di-load
setPerkuliahan();

// set perkuliahan
function setPerkuliahan() {
  const perkuliahanContainer = document.getElementById("perkuliahanContainer");
  const perkuliahanData = document.getElementById("perkuliahanData");
  const perkuliahan = JSON.parse(perkuliahanData.textContent);

  perkuliahan.forEach((item) => {
    const col = document.createElement("div");
    col.className = "col mb-4 stretch-card transparent";
    const card = document.createElement("div");
    card.className = "card card-tale";
    const cardBody = document.createElement("div");
    cardBody.className = "card-body";
    cardBody.innerHTML = `
      <h6 class="mt-2 mb-4">Ruang ${item.ruangan}</h6>
      <h3 class="my-3 font-weight-bold">${item.matkul}</h3>
      <h6 class="my-3">${item.jam_mulai} - ${item.jam_selesai}</h6>
      <button type="button" class="btn btn-outline-primary btn-fw btn-block" onclick="linimasa(${item.id_perkuliahan})">Detail</button>
    `;
    card.appendChild(cardBody);
    col.appendChild(card);
    perkuliahanContainer.appendChild(col);
  });
}

// load linimasa
function linimasa(id_perkuliahan) {
  window.location.href = "/perkuliahan/jadwal/linimasa/" + id_perkuliahan;
}
