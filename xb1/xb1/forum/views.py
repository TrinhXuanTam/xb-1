from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView


from ..articles.models import ForumCategory, Forum, Comment
from ..core.views import LoginMixinView


class ForumIndexView(TemplateView):

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

    
class ForumListView(TemplateView):

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


class ForumDetailView(TemplateView):

    template_name = "forum_detail.html"

    def get_context_data(self, *args, **kwargs):

        context = super(ForumDetailView, self).get_context_data(*args, **kwargs)

        pk = kwargs.get("pk", None)
        context["object"] = Forum.objects.get(pk=pk)
        
        return context


class ForumCreateView(CreateView):

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