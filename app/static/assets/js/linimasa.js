function renderTimeline(timelineElements) {
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
      // presensi belum ditandai
      case "3":
        bg_color = "bg-warning";
        icon = "ti-alert text-white";
        break;
      // presensi ditandai
      case "4":
        bg_color = "bg-success";
        icon = "ti-check text-white";
        break;
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
    li.className = "timeline-item mb-5";
    li.id = "timeline-item-" + element.id_title;
    const span = document.createElement("span"); // create span element inside li
    span.className = "timeline-icon " + bg_color;
    // span.className = "timeline-icon";
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
      li.appendChild(renderPresensiSection());
    }

    ul.appendChild(li);
  });
}

// render prensensi section when id_title == 2
function renderPresensiSection() {
  const presensiSection = document.createElement("div");
  presensiSection.id = "presensi-section";
  const presensiText = document.createElement("p");
  presensiText.textContent = "Presensi telah dibuka, klik tombol dibawah ini untuk melakukan presensi";
  const presensiButton = document.createElement("button");
  presensiButton.id = "presensi-button";
  presensiButton.className = "btn btn-primary";
  presensiButton.textContent = "Tandai kehadiran";
  presensiSection.appendChild(presensiText);
  presensiSection.appendChild(presensiButton);
  return presensiSection;
}
