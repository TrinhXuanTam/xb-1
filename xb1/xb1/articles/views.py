from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render
from django.http import HttpResponse

from .forms import ArticleForm
from .models import Article, Comment
from ..core.models import Profile
from ..core.views import LoginMixinView


class ArticleListView(LoginMixinView, ListView):
    model = Article
    template_name = "articles.html"


class ArticleCreateView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    template_name = "articles_form.html"
    form_class = ArticleForm
    success_url = reverse_lazy("articles:article_list")
    permission_required = "articles.add_article"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ArticleCreateView, self).form_valid(form)


class ArticleUpdateView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = Article
    template_name = "articles_form.html"
    form_class = ArticleForm
    success_url = reverse_lazy("articles:article_list")
    permission_required = "articles.change_article"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ArticleUpdateView, self).form_valid(form)

class ArticleDetailView(LoginMixinView, DetailView):
    model = Article
    template_name = "articles_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        article = Article.objects.get(slug=kwargs['slug'])
        comments = None
        if article.allow_comments:
            comments = Comment.objects.filter(article=article.id, reaction_to_id=None)
            # Get comments with user data
            for comment in comments:
                comment.user = Profile.objects.get(user_id=comment.author_id)
                # Get replies to given comment
                comment.replies = Comment.objects.filter(reaction_to_id=comment.id)
                for reply in comment.replies:
                    reply.user = Profile.objects.get(user_id=reply.author_id)
        context['article'] = article
        context['comments'] = comments
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return render(request, 'articles_detail.html', self.get_context_data(*args, **kwargs))

