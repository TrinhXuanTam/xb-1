from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView


from ..articles.models import ForumCategory, Forum, Comment
from ..core.views import LoginMixinView
from ..core.models import Profile


class ForumIndexView(LoginMixinView, TemplateView):
    """
    View shows list of all categories and last active forum in a category.
    """

    template_name = "forum_index.html"


    def get_context_data(self, *args, **kwargs):

        context = super(ForumIndexView, self).get_context_data(*args, **kwargs)

        context["categories"] = list(ForumCategory.objects.all().order_by('title'))

        for category in context["categories"]:
            category.latest = Forum.objects.filter(category=category.id).last()

        context["categories"].insert(0, {
            "title": _("All forums"),
            "latest": Forum.objects.filter().last(),
            "pk": False
        })

        return context


class ForumListView(LoginMixinView, TemplateView):
    """
    View lists all forums in selected category.
    """

    template_name = "forum_list.html"

    def get_context_data(self, *args, **kwargs):

        context = super(ForumListView, self).get_context_data(*args, **kwargs)

        pk = kwargs.get('pk', None)
        if pk:
            context["forums"] = Forum.objects.filter(category__pk=pk)
            context["title"] = ForumCategory.objects.get(pk=pk).title
            context["is_open"] = ForumCategory.objects.get(pk=pk).is_open
            context["category_pk"] = pk
        else:
            context["forums"] = Forum.objects.all()
            context["title"] = _("Last forums")
            context["is_open"] = False
            context["category_pk"] = False

        for forum in context["forums"]:
            querySet = Comment.objects.filter(forum=forum)
            forum.replies_cnt = querySet.count()
            try:
                forum.last_date = querySet.latest('date').date
            except Comment.DoesNotExist:
                forum.last_date = '-'

        return context


class ForumCategoryCreateView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    View creates new forum category.
    """

    template_name = "forum_category_form.html"
    success_url = reverse_lazy("forum:index")
    permission_required = "articles.add_forumcategory"
    model = ForumCategory
    fields = ("title", "is_open", "description")

    def form_valid(self, form):
        return super(ForumCategoryCreateView, self).form_valid(form)


class ForumCategoryUpdateView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    View for editing existing forum category.
    """

    template_name = "forum_category_form.html"
    success_url = reverse_lazy("forum:index")
    permission_required = "articles.change_forumcategory"
    model = ForumCategory
    fields = ("title", "is_open", "description")


class ForumDetailView(LoginMixinView, TemplateView):
    """
    Forum displays text of the forum title
    and comments under it.
    """

    template_name = "forum_detail.html"

    def get_context_data(self, *args, **kwargs):

        context = super(ForumDetailView, self).get_context_data(*args, **kwargs)

        pk = kwargs.get("pk", None)
        context["object"] = Forum.objects.get(pk=pk)

        context["comments"] = []

        q_comments = Comment.objects.filter(forum=context["object"], reaction_to=None)

        for comment in q_comments:
            context["comments"].append({
                "author": comment.author,
                "text": comment.text,
                "date": comment.date,
                "id": comment.pk,
                "comments": self.get_comment_childs(comment),
                "is_censured": comment.is_censured
            })

        context["forum_id"] = context["object"].pk

        return context

    def get_comment_childs(self, parent):

        res = []

        for comment in parent.comment_set.all():
            res.append({
                "author": comment.author,
                "text": comment.text,
                "date": comment.date,
                "id": comment.pk,
                "comments": self.get_comment_childs(comment),
                "is_censured": comment.is_censured
            })

        return res


class PostCommentView(LoginRequiredMixin, View):
    """
    View handles requests for creating new comments.
    """

    def post(self, request, *args, **kwargs):

        if request.user.is_authenticated:

            forum_id = int(request.POST.get('forum_id'))
            reaction_to_id = int(request.POST.get('comment_id'))
            text = request.POST.get('text')
            comment = Comment(
                text=text,
                author_id=request.user.id,
                forum_id=forum_id,
            )
            if reaction_to_id >= 0:
                comment.reaction_to_id=reaction_to_id

            comment.save()
            comment.user = Profile.objects.get(user_id=request.user.id)
            return render(request, 'forum_comment.html', {"forum_id":forum_id, "comments":[comment]})

        else:
            response = JsonResponse({"error": _("Unauthorized")})
            response.status_code = 401
            return response


class ForumCreateView(LoginMixinView, LoginRequiredMixin, CreateView):
    """
    View handles form which creates a new forum.
    """

    template_name = "forum_form.html"
    success_url = reverse_lazy("forum:index")
    model = Forum
    fields = ("title", "description")

    def dispatch(self, request, *args, **kwargs):

        category = ForumCategory.objects.get(pk=self.kwargs.get("pk", None))

        if not category.is_open and not self.request.user.has_perm("articles.add_forum"):
            return HttpResponseRedirect(reverse_lazy("forum:index"))
        else:
            return super(ForumCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        category = ForumCategory.objects.get(pk=self.kwargs.get("pk", None))

        form.instance.author = self.request.user
        form.instance.category = category
        form.instance.is_closed = False

        form.instance.save()

        return super(ForumCreateView, self).form_valid(form)
