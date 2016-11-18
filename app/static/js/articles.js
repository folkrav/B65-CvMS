$(document).ready(function() {
    $("#tags").select2({
        placeholder: "Choisir des tags",
        allowClear: true,
        tokenSeparators: [",", " "]
    });
});
