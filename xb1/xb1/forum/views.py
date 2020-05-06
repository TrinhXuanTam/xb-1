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

    template_name = "forum_index.html"


    def get_context_data(self, *args, **kwargs):

        context = super(ForumIndexView, self).get_context_data(*args, **kwargs)

        context["categories"] = []

        context["categories"].append({
            "title": _("Last forums"),
            "forums": Forum.objects.all()[:5],
            "url": reverse_lazy("forum:forum_list"),
            "pk": False
        })

        for category in ForumCategory.objects.all():

            c = {
                "title": category.title,
                "forums": [],
                "url": reverse_lazy("forum:forum_list", kwargs={"pk": category.pk}),
                "pk": category.pk
            }

            for forum in category.forum_set.all()[:5]: # Get only five results // TODO filter 5 with last activity (last comments)
                c["forums"].append(forum)

            context["categories"].append(c)

        return context

    
class ForumListView(LoginMixinView, TemplateView):

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
        
        return context


class ForumCategoryCreateView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    template_name = "forum_category_form.html"
    success_url = reverse_lazy("forum:index")
    permission_required = "articles.add_forumcategory"
    model = ForumCategory
    fields = ("title", "is_open")

    def form_valid(self, form):
        return super(ForumCategoryCreateView, self).form_valid(form)


class ForumCategoryUpdateView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    template_name = "forum_category_form.html"
    success_url = reverse_lazy("forum:index")
    permission_required = "articles.change_forumcategory"
    model = ForumCategory
    fields = ("title", "is_open")


class ForumDetailView(LoginMixinView, TemplateView):

    template_name = "forum_detail.html"

    def get_context_data(self, *args, **kwargs):

        context = super(ForumDetailView, self).get_context_data(*args, **kwargs)

        pk = kwargs.get("pk", None)
        context["object"] = Forum.objects.get(pk=pk)

        context["comments"] = []

        q_comments = Comment.objects.filter(forum=context["object"], reaction_to=None)

        for comment in q_comments:
            context["comments"].append({
                "author": comment.author.profile,
                "text": comment.text,
                "date": comment.date,
                "id": comment.pk,
                "comments": self.get_comment_childs(comment)
            })
        
        return context

    def get_comment_childs(self, parent):

        res = []

        for comment in parent.comment_set.all():
            res.append({
                "author": comment.author.profile,
                "text": comment.text,
                "date": comment.date,
                "id": comment.pk,
                "comments": self.get_comment_childs(comment)
            })
        
        return res


class PostCommentView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        if request.user.is_authenticated:
    
            forum_id = int(request.POST.get('forum_id'))
            reaction_to_id = int(request.POST.get('comment_id'))
            text = request.POST.get('text')
            comment = Comment(
                text=text,
                author_id=request.user.id,
                forum_id=forum_id,
                reaction_to_id=reaction_to_id
            )
            comment.save()
            comment.user = Profile.objects.get(user_id=request.user.id)
            return render(request, 'new_reply.html', {"reply":comment})
    
        else:
            response = JsonResponse({"error": "Unauthorized"})
            response.status_code = 401
            return response


class ForumCreateView(LoginMixinView, CreateView):

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