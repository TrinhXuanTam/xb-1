from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render
from django.http import HttpResponse

from .forms import ArticleForm
from .models import Article
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
        
def article_detail(request, slug):
    article = Article.objects.get(slug=slug)
    return render(request, 'articles_detail.html', {'article': article})

