$(".slider_next").click(function() {
    $('.articles_categories_wrapper').animate({'margin-left':'-=190px'}, 200);
})

$(".slider_back").click(function() {
    $('.articles_categories_wrapper').animate({'margin-left':'+=190px'}, 200);
})