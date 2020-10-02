var comment_textarea = document.querySelectorAll('#comment_post_form textarea, .comment_reply_form textarea');

comment_textarea.forEach(function(node) {
  node.setAttribute('style', 'height:' + (comment_textarea.scrollHeight) + 'px;overflow-y:hidden;');
  node.addEventListener("input", OnInput, false);
})

function OnInput() {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
}

$(".comment_reply_form textarea").hide()
$(".comment_reply_form .comment_section_button").click(function() {
  $(this).parent().find("textarea").show()
}) 