var comment_textarea = document.querySelector('.comment_post_form textarea');
comment_textarea.setAttribute('style', 'height:' + (comment_textarea.scrollHeight) + 'px;overflow-y:hidden;');
comment_textarea.addEventListener("input", OnInput, false);

function OnInput() {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
}