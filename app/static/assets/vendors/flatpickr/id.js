/* Indonesian locals for flatpickr */
var fp =
  typeof window !== "undefined" && window.flatpickr !== undefined
    ? window.flatpickr
    : {
        l10ns: {},
      };
var Indonesian = {
  weekdays: {
    shorthand: ["Min", "Sen", "Sel", "Rab", "Kam", "Jum", "Sab"],
    longhand: ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"],
  },
  months: {
    shorthand: ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"],
    longhand: ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"],
  },
  firstDayOfWeek: 1,
  ordinal: function () {
    return "";
  },
  time_24hr: true,
  rangeSeparator: " - ",
};
fp.l10ns.id = Indonesian;
module.exports = fp.l10ns;
