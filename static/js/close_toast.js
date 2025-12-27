$(document).ready(function () {
    $(".message-close").on("click", function () {
        $(this).parent(".message").fadeOut(300, function () {
            $(this).remove();
        });
    });
});
