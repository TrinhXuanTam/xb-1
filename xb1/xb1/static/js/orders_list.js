$(".delete-order-button").click(function(e) {
    e.preventDefault();
    var email = $(this).closest('tr').find('.order-email').html();
    var url = $(this).attr('href')

    $('#login_modal').find('strong').html(email);
    $('#login_modal').find('form').attr('action', url);
    openDialog();
})