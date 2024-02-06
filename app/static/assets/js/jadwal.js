function selectedKelas() {
  const kelas = document.getElementById("inputKelas").value;
  return kelas;
}

function selectedIndexelectedMk() {
  const mk = document.getElementById("inputMataKuliah").value;
  return mk;
}

// get pertemuan ke- untuk form tambah jadwal
function getPertemuan() {
  const kelas = selectedKelas();
  const mk = selectedIndexelectedMk();

  if (kelas && mk) {
    fetch("perkuliahan/jadwal/get_pertemuan/" + kelas + "/" + mk)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        const pertemuanField = document.getElementById("inputPertemuan");
        pertemuanField.innerHTML = data.data;
        pertemuanField.value = data.data;
      })
      .catch((error) => {
        console.error("There has been a problem with your fetch operation:", error);
      });
  }
}

// detail perkuliahan
function perkuliahanDetail(event) {
  const dataPerkuliahan = event.extendedProps.customData || {};
  document.getElementById("detailKelas").value = dataPerkuliahan["kelas"];
  document.getElementById("detailMK").value = dataPerkuliahan["mataKuliah"];
  document.getElementById("detailPertemuan").value = dataPerkuliahan["pertemuan"];
  document.getElementById("detailRuangan").value = dataPerkuliahan["ruangan"];
  document.getElementById("detailTanggal").value = dataPerkuliahan["tanggal"];
  document.getElementById("detailJamMulai").value = dataPerkuliahan["jamMulai"];
  document.getElementById("detailJamSelesai").value = dataPerkuliahan["jamSelesai"];

  // document.getElementById("editPerkuliahanForm").action = "/perkuliahan/jadwal/detail/" + event.id;
  // document.getElementById("editPerkuliahanForm").action = "{{ url_for('perkuliahan_blueprint.jadwal', id='" + event.id + "') }}";
  $("#modalDetailPerkuliahan").modal("show");
}

// enable fields untuk edit detail perkuliahan
function enableEditDataFields() {
  document.getElementById("detailRuangan").removeAttribute("disabled");
  document.getElementById("detailTanggal").removeAttribute("disabled");
  document.getElementById("detailJamMulai").removeAttribute("disabled");
  document.getElementById("detailJamSelesai").removeAttribute("disabled");
  document.getElementById("btnDetail").style.display = "none";
  document.getElementById("btnEditDetail").style.display = "block";
}

function submitEditForm() {
  // document.getElementById("editPerkuliahanForm").submit();
  document.getElementById("detailRuangan").setAttribute("disabled", "disabled");
  document.getElementById("detailTanggal").setAttribute("disabled", "disabled");
  document.getElementById("detailJamMulai").setAttribute("disabled", "disabled");
  document.getElementById("detailJamSelesai").setAttribute("disabled", "disabled");
  document.getElementById("btnDetail").style.display = "block";
  document.getElementById("btnEditDetail").style.display = "none";
}
