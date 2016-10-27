$(document).ready(function () {
    $(".alert").each(function (index) {
        $(this).delay(index*600).slideDown(400).delay(3500).slideUp(400);
    })
});
