(function ($) {
  "use strict";
  // if ($("#timepicker-example").length) {
  //   $("#timepicker-example").datetimepicker({
  //     format: "LT",
  //     format: "HH:mm",
  //   });
  // }
  if ($(".timepicker-example").length) {
    $(".timepicker-example").datetimepicker({
      format: "LT",
      format: "HH:mm",
    });
  }
  if ($(".color-picker").length) {
    $(".color-picker").asColorPicker();
  }
  if ($("#datepicker-popup").length) {
    $("#datepicker-popup").datepicker({
      enableOnReadonly: true,
      todayHighlight: true,
      language: "id",
      daysOfWeekDisabled: [0, 6],
    });
  }
  if ($("#inline-datepicker").length) {
    $("#inline-datepicker").datepicker({
      enableOnReadonly: true,
      todayHighlight: true,
      locale: "id",
    });
  }
  if ($(".datepicker-autoclose").length) {
    $(".datepicker-autoclose").datepicker({
      autoclose: true,
      locale: "id",
    });
  }
  if ($('input[name="date-range"]').length) {
    $('input[name="date-range"]').daterangepicker();
  }
  if ($(".input-daterange").length) {
    $(".input-daterange input").each(function () {
      $(this).datepicker("clearDates");
    });
    $(".input-daterange").datepicker({});
  }
})(jQuery);
