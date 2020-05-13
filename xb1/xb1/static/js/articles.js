var child_index = 0 
var children_cnt = $('.articles_categories_wrapper').children().length

$(".slider_next").click(function() {
    if (child_index > children_cnt - 2)
        return

    off = $('.articles_categories_wrapper').children().eq(child_index).innerWidth()
    $('.articles_categories_wrapper').animate({'margin-left':'-=' + off + 'px'}, 200);
    child_index += 1
})

$(".slider_back").click(function() {
    if (child_index == 0)
        return
    child_index -=1 
    off = $('.articles_categories_wrapper').children().eq(child_index).innerWidth()
    $('.articles_categories_wrapper').animate({'margin-left':'+=' + off + 'px'}, 200);
})

$(".article_category").click(function() {
    if($(this).hasClass('article_category_active'))
        return

    $('.article_category').removeClass("article_category_active")
    $(this).addClass('article_category_active')

})